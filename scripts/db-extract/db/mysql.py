"""MySQL database client."""

import pymysql
import pandas as pd

from .base import DatabaseClient, DatabaseConfig, _validate_identifier


class MySQLClient(DatabaseClient):
    """MySQL implementation using PyMySQL."""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._connection = None

    def connect(self) -> None:
        self._connection = pymysql.connect(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def disconnect(self) -> None:
        if self._connection:
            self._connection.close()
            self._connection = None

    def query(self, sql: str) -> pd.DataFrame:
        if not self._connection:
            self.connect()
        return pd.read_sql(sql, self._connection)

    def get_columns(self, table: str) -> list[str]:
        _validate_identifier(table, "table")
        with self._connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            return [row["Field"] for row in cursor.fetchall()]
