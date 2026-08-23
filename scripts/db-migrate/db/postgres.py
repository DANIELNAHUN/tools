"""PostgreSQL database client - stub for future implementation."""

from .base import DatabaseClient, DatabaseConfig


class PostgreSQLClient(DatabaseClient):
    def connect(self) -> None:
        raise NotImplementedError("PostgreSQL support coming soon")

    def disconnect(self) -> None:
        raise NotImplementedError("PostgreSQL support coming soon")

    def query(self, sql: str):
        raise NotImplementedError("PostgreSQL support coming soon")

    def insert_dataframe(self, table: str, df) -> int:
        raise NotImplementedError("PostgreSQL support coming soon")

    def table_exists(self, table: str) -> bool:
        raise NotImplementedError("PostgreSQL support coming soon")
