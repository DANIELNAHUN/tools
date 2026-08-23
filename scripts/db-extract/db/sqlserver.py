"""SQL Server database client - stub for future implementation."""

from .base import DatabaseClient, DatabaseConfig


class SQLServerClient(DatabaseClient):
    """SQL Server implementation using pyodbc."""

    def connect(self) -> None:
        raise NotImplementedError("SQL Server support coming soon")

    def disconnect(self) -> None:
        raise NotImplementedError("SQL Server support coming soon")

    def query(self, sql: str):
        raise NotImplementedError("SQL Server support coming soon")

    def get_columns(self, table: str) -> list[str]:
        raise NotImplementedError("SQL Server support coming soon")
