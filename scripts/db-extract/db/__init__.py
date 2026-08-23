"""Database abstraction layer."""

from .base import DatabaseClient, DatabaseConfig
from .mysql import MySQLClient

DATABASES = {
    "mysql": MySQLClient,
    # "postgres": PostgreSQLClient,  # TODO: implement
    # "sqlserver": SQLServerClient,  # TODO: implement
}


def get_client(db_type: str, config: DatabaseConfig) -> DatabaseClient:
    """Factory to get the appropriate database client."""
    if db_type not in DATABASES:
        available = ", ".join(DATABASES.keys())
        raise ValueError(f"Unsupported database '{db_type}'. Available: {available}")
    return DATABASES[db_type](config)
