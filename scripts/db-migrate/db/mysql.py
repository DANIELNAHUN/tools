"""MySQL database client."""

import pymysql
import pandas as pd

from .base import DatabaseClient, DatabaseConfig


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

    def insert_dataframe(self, table: str, df: pd.DataFrame) -> int:
        """Insert DataFrame rows into table. Returns count inserted."""
        if not self._connection:
            self.connect()

        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self._connection.cursor() as cursor:
            rows = [tuple(row) for _, row in df.iterrows()]
            cursor.executemany(sql, rows)
            self._connection.commit()
            return len(rows)

    def table_exists(self, table: str) -> bool:
        if not self._connection:
            self.connect()
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = %s AND table_name = %s",
                (self.config.database, table),
            )
            return cursor.fetchone()["COUNT(*)"] > 0

    def get_columns(self, table: str) -> list[str]:
        with self._connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            return [row["Field"] for row in cursor.fetchall()]
