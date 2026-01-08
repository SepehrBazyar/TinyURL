import logging

import psycopg2

from .base import BaseManager
from ..exceptions import (
    DuplicateDataError,
    NotExistError,
)

logger = logging.getLogger(__name__)


class DBManager(BaseManager):
    def __init__(
        self,
        db_name: str,
        *,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        password: str = "postgres",
    ):
        self.connection = self._connect(
            params={
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "dbname": db_name
            },
        )

    def create(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id SERIAL PRIMARY KEY,
                    original_url TEXT NOT NULL,
                    short_code VARCHAR(8) UNIQUE NOT NULL
                );
            """)
            self.connection.commit()

    def read(self, short_code):
        with self.connection.cursor() as cur:
            cur.execute(
                """
                    SELECT original_url FROM urls WHERE short_code = %s;
                """,
                (
                    short_code,
                ),
            )
            result = cur.fetchone()
            if not result:
                raise NotExistError("No Value")

            return result[0]

    def write(self, url, short_code):
        with self.connection.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO urls (original_url, short_code)
                    VALUES (%s, %s);
                """,
                (
                    url,
                    short_code,
                ),
            )
            try:
                self.connection.commit()
            except psycopg2.IntegrityError:
                self.connection.rollback()
                raise DuplicateDataError("Duplicate Short Code")

    def _connect(self, params: dict):
        try:
            return psycopg2.connect(**params)
        except Exception as e:
            logger.exception(e)

    def _close(self):
        if self.connection is not None:
            self.connection.close()


db_manager = DBManager("tiny_url")
db_manager.create()
