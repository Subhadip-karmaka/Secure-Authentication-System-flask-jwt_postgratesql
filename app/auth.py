from __future__ import annotations

from datetime import datetime, timezone
from functools import wraps
from typing import Callable

import jwt
from flask import Blueprint, current_app, g, jsonify, request
from psycopg2 import IntegrityError

from .security import create_access_token, decode_token, hash_password, verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _extract_bearer_token(header_value: str | None) -> str | None:
    if not header_value:
        return None
    parts = header_value.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


def token_required(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_bearer_token(request.headers.get("Authorization"))
        if not token:
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        try:
            payload = decode_token(token, current_app.config["JWT_SECRET_KEY"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        jti = payload.get("jti")
        with current_app.db.cursor() as cur:
            cur.execute("SELECT revoked_at FROM token_blacklist WHERE jti = %s", (jti,))
            revoked = cur.fetchone()
            if revoked:
                return jsonify({"error": "Token has been revoked"}), 401

        g.current_user = {
            "id": int(payload["sub"]),
            "email": payload["email"],
            "jti": jti,
        }
        return fn(*args, **kwargs)

    return wrapper


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    password_hash = hash_password(password)

    try:
        with current_app.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email, created_at
                """,
                (email, password_hash),
            )
            user = cur.fetchone()
    except IntegrityError as exc:
        if "duplicate key value violates unique constraint" in str(exc).lower():
            return jsonify({"error": "Email is already registered"}), 409
        raise

    return (
        jsonify(
            {
                "message": "Registration successful",
                "user": {"id": user[0], "email": user[1], "created_at": user[2].isoformat()},
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    with current_app.db.cursor() as cur:
        cur.execute(
            "SELECT id, email, password_hash FROM users WHERE email = %s",
            (email,),
        )
        user = cur.fetchone()

    if not user or not verify_password(password, user[2]):
        return jsonify({"error": "Invalid credentials"}), 401

    token, jti = create_access_token(
        user_id=user[0],
        email=user[1],
        secret_key=current_app.config["JWT_SECRET_KEY"],
        expires_minutes=current_app.config["JWT_ACCESS_TOKEN_MINUTES"],
    )

    with current_app.db.cursor() as cur:
        cur.execute(
            "UPDATE users SET last_login_at = NOW() WHERE id = %s",
            (user[0],),
        )

    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in_minutes": current_app.config["JWT_ACCESS_TOKEN_MINUTES"],
            "jti": jti,
        }
    )


@auth_bp.get("/me")
@token_required
def me():
    with current_app.db.cursor() as cur:
        cur.execute(
            """
            SELECT id, email, created_at, last_login_at
            FROM users
            WHERE id = %s
            """,
            (g.current_user["id"],),
        )
        user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "id": user[0],
            "email": user[1],
            "created_at": user[2].isoformat(),
            "last_login_at": user[3].isoformat() if user[3] else None,
        }
    )


@auth_bp.post("/logout")
@token_required
def logout():
    now = datetime.now(timezone.utc)
    with current_app.db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO token_blacklist (jti, user_id, revoked_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (jti) DO NOTHING
            """,
            (g.current_user["jti"], g.current_user["id"], now),
        )
    return jsonify({"message": "Logged out successfully"})
