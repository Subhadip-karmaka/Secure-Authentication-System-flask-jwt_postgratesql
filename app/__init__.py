from __future__ import annotations

from flask import Flask, jsonify
from flask_cors import CORS

from .auth import auth_bp
from .config import load_settings
from .db import Database


def create_app() -> Flask:
    settings = load_settings()

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_MINUTES"] = settings.jwt_access_token_minutes

    app.db = Database(dsn=settings.db_dsn)

    CORS(
        app,
        resources={r"/api/*": {"origins": settings.cors_allowed_origins}},
        supports_credentials=False,
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.get("/api/health")
    def health() -> tuple:
        return jsonify({"status": "ok"}), 200

    app.register_blueprint(auth_bp)

    @app.errorhandler(500)
    def handle_500(_):
        return jsonify({"error": "Internal server error"}), 500

    return app
