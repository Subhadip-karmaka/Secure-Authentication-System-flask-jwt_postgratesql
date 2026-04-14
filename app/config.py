from __future__ import annotations

import os
from dataclasses import dataclass


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    flask_env: str
    debug: bool
    host: str
    port: int
    jwt_secret_key: str
    jwt_access_token_minutes: int
    cors_allowed_origins: list[str]
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def db_dsn(self) -> str:
        return (
            f"host={self.db_host} "
            f"port={self.db_port} "
            f"dbname={self.db_name} "
            f"user={self.db_user} "
            f"password={self.db_password}"
        )


def load_settings() -> Settings:
    cors_raw = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
    )
    origins = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]

    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "")
    if not jwt_secret_key:
        raise ValueError("JWT_SECRET_KEY is required. Set it in your environment.")

    return Settings(
        flask_env=os.getenv("FLASK_ENV", "development"),
        debug=_to_bool(os.getenv("FLASK_DEBUG"), default=True),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        jwt_secret_key=jwt_secret_key,
        jwt_access_token_minutes=int(os.getenv("JWT_ACCESS_TOKEN_MINUTES", "15")),
        cors_allowed_origins=origins,
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "5432")),
        db_name=os.getenv("DB_NAME", "auth_system"),
        db_user=os.getenv("DB_USER", "postgres"),
        db_password=os.getenv("DB_PASSWORD", "postgres"),
    )
