from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from psycopg2.pool import SimpleConnectionPool


class Database:
    def __init__(self, dsn: str, minconn: int = 1, maxconn: int = 10) -> None:
        self._pool = SimpleConnectionPool(minconn=minconn, maxconn=maxconn, dsn=dsn)

    @contextmanager
    def connection(self) -> Generator:
        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)

    @contextmanager
    def cursor(self) -> Generator:
        with self.connection() as conn:
            with conn.cursor() as cur:
                try:
                    yield cur
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise

    def close(self) -> None:
        self._pool.closeall()
