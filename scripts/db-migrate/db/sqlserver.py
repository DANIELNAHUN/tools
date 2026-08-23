"""SQL Server database client - stub for future implementation."""

from .base import DatabaseClient, DatabaseConfig


class SQLServerClient(DatabaseClient):
    def connect(self) -> None:
        raise NotImplementedError("SQL Server support coming soon")

    def disconnect(self) -> None:
        raise NotImplementedError("SQL Server support coming soon")

    def query(self, sql: str):
        raise NotImplementedError("SQL Server support coming soon")

    def insert_dataframe(self, table: str, df) -> int:
        raise NotImplementedError("SQL Server support coming soon")

    def table_exists(self, table: str) -> bool:
        raise NotImplementedError("SQL Server support coming soon")
