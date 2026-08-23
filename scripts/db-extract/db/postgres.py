"""PostgreSQL database client - stub for future implementation."""

from .base import DatabaseClient, DatabaseConfig


class PostgreSQLClient(DatabaseClient):
    """PostgreSQL implementation using psycopg2."""

    def connect(self) -> None:
        raise NotImplementedError("PostgreSQL support coming soon")

    def disconnect(self) -> None:
        raise NotImplementedError("PostgreSQL support coming soon")

    def query(self, sql: str):
        raise NotImplementedError("PostgreSQL support coming soon")

    def get_columns(self, table: str) -> list[str]:
        raise NotImplementedError("PostgreSQL support coming soon")
