"""Abstract database client interface."""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

_IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$")


def _validate_identifier(name: str, label: str = "identifier") -> str:
    """Raise ValueError if *name* is not a safe SQL identifier."""
    if not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid {label}: {name!r}")
    return name


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
    def get_columns(self, table: str) -> list[str]:
        """Get column names for a table."""

    def fetch_table(
        self, table: str, fields: list[str] | None = None
    ) -> pd.DataFrame:
        """Fetch data from a table with optional field selection."""
        _validate_identifier(table, "table")
        cols = ", ".join(fields) if fields else "*"
        if fields:
            for f in fields:
                _validate_identifier(f, "field")
        sql = f"SELECT {cols} FROM {table}"
        return self.query(sql)
