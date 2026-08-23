"""Extract data from databases to CSV/XLSX.

Usage:
    uv run extract.py --db mysql --config config.yaml
    uv run extract.py --config config.yaml          # defaults to mysql
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
    """Load extraction configuration from YAML."""
    path = Path(config_path)
    if not path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def run_extraction(db_type: str, config: dict) -> None:
    """Execute all extractions defined in config."""
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", ""),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
    )

    client = get_client(db_type, db_config)

    try:
        client.connect()
        print(f"Connected to {db_type}")

        for extraction in config.get("extractions", []):
            name = extraction["name"]
            table = extraction["table"]
            fields = extraction.get("fields")
            fmt = extraction.get("output_format", "csv")
            output = extraction.get("output_file", f"output/{name}.{fmt}")

            print(f"\n--- {name} ---")
            print(f"Table: {table}")
            print(f"Fields: {fields or '*'}")
            print(f"Format: {fmt}")

            df = client.fetch_table(table, fields)
            print(f"Rows fetched: {len(df)}")

            # Ensure output directory exists
            Path(output).parent.mkdir(parents=True, exist_ok=True)

            if fmt == "xlsx":
                df.to_excel(output, index=False, engine="openpyxl")
            else:
                df.to_csv(output, index=False)

            print(f"Saved to: {output}")

    finally:
        client.disconnect()
        print("\nDisconnected.")


def main():
    parser = argparse.ArgumentParser(
        description="Extract data from databases to CSV/XLSX"
    )
    parser.add_argument(
        "--db",
        choices=["mysql", "postgres", "sqlserver"],
        default="mysql",
        help="Database type (default: mysql)",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to extraction config YAML (default: config.yaml)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    run_extraction(args.db, config)


if __name__ == "__main__":
    main()
