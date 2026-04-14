from __future__ import annotations

from dotenv import load_dotenv

from app import create_app
from app.config import load_settings

load_dotenv()
settings = load_settings()

print("DB DSN =", settings.db_dsn)

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
