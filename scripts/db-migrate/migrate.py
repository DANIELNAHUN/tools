"""Migrate data between databases.

Usage:
    uv run migrate.py --source mysql --target mysql
    uv run migrate.py --source mysql --target postgres --mapping mapping.yaml
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from db import get_client, DatabaseConfig

load_dotenv()


def load_config(config_path: str) -> dict:
    """Load migration configuration from YAML."""
    path = Path(config_path)
    if not path.exists():
        print(f"Error: Mapping file not found: {config_path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def build_config(prefix: str) -> DatabaseConfig:
    """Build DatabaseConfig from env vars with given prefix."""
    return DatabaseConfig(
        host=os.getenv(f"{prefix}_DB_HOST", "localhost"),
        port=int(os.getenv(f"{prefix}_DB_PORT", "3306")),
        database=os.getenv(f"{prefix}_DB_NAME", ""),
        user=os.getenv(f"{prefix}_DB_USER", ""),
        password=os.getenv(f"{prefix}_DB_PASSWORD", ""),
    )


def run_migration(source_type: str, target_type: str, config: dict) -> None:
    """Execute all migrations defined in config."""
    source_config = build_config("SOURCE")
    target_config = build_config("TARGET")

    source_client = get_client(source_type, source_config)
    target_client = get_client(target_type, target_config)

    try:
        source_client.connect()
        print(f"Connected to source ({source_type}: {source_config.database})")

        target_client.connect()
        print(f"Connected to target ({target_type}: {target_config.database})")

        for migration in config.get("migrations", []):
            name = migration["name"]
            source_table = migration["source_table"]
            target_table = migration["target_table"]
            field_mapping = migration.get("field_mapping", {})

            print(f"\n--- {name} ---")
            print(f"Source: {source_table} -> Target: {target_table}")

            if not target_client.table_exists(target_table):
                print(f"  [SKIP] Target table '{target_table}' does not exist")
                continue

            df = source_client.fetch_table(source_table)
            print(f"  Rows fetched: {len(df)}")

            if field_mapping:
                # Rename columns based on mapping
                rename = {src: tgt for src, tgt in field_mapping.items()}
                df = df[list(rename.keys())].rename(columns=rename)
                print(f"  Fields mapped: {list(rename.values())}")

            inserted = target_client.insert_dataframe(target_table, df)
            print(f"  Rows inserted: {inserted}")

    finally:
        source_client.disconnect()
        target_client.disconnect()
        print("\nAll connections closed.")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate data between databases"
    )
    parser.add_argument(
        "--source",
        choices=["mysql", "postgres", "sqlserver"],
        default="mysql",
        help="Source database type (default: mysql)",
    )
    parser.add_argument(
        "--target",
        choices=["mysql", "postgres", "sqlserver"],
        default="mysql",
        help="Target database type (default: mysql)",
    )
    parser.add_argument(
        "--mapping",
        default="mapping.yaml",
        help="Path to migration mapping YAML (default: mapping.yaml)",
    )
    args = parser.parse_args()

    config = load_config(args.mapping)
    run_migration(args.source, args.target, config)


if __name__ == "__main__":
    main()
