"""Abstract database client interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


class DatabaseClient(ABC):
    """Base class for all database clients."""

    def __init__(self, config: DatabaseConfig):
        self.config = config

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection."""

    @abstractmethod
    def query(self, sql: str) -> pd.DataFrame:
        """Execute a query and return results as a DataFrame."""

    @abstractmethod
    def insert_dataframe(self, table: str, df: pd.DataFrame) -> int:
        """Insert a DataFrame into a table. Returns rows inserted."""

    @abstractmethod
    def table_exists(self, table: str) -> bool:
        """Check if a table exists."""

    def fetch_table(
        self, table: str, fields: list[str] | None = None
    ) -> pd.DataFrame:
        """Fetch data from a table with optional field selection."""
        cols = ", ".join(fields) if fields else "*"
        sql = f"SELECT {cols} FROM {table}"
        return self.query(sql)
