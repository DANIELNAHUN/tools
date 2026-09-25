"""MySQL database client."""

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL, Engine

from .base import DatabaseClient, DatabaseConfig, _validate_identifier


class MySQLClient(DatabaseClient):
    """MySQL implementation using SQLAlchemy and PyMySQL."""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._engine: Engine | None = None

    def connect(self) -> None:
        url = URL.create(
            drivername="mysql+pymysql",
            username=self.config.user or None,
            password=self.config.password or None,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
        )
        self._engine = create_engine(url)
        with self._engine.connect():
            pass

    def disconnect(self) -> None:
        if self._engine:
            self._engine.dispose()
            self._engine = None

    def query(self, sql: str) -> pd.DataFrame:
        if not self._engine:
            self.connect()
        with self._engine.connect() as conn:
            return pd.read_sql_query(text(sql), conn)

    def get_columns(self, table: str) -> list[str]:
        _validate_identifier(table, "table")
        if not self._engine:
            self.connect()
        inspector = inspect(self._engine)
        return [col["name"] for col in inspector.get_columns(table)]

