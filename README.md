# tools

Colección de scripts utilitarios para extracción de datos, migración y análisis de repositorios.

## Estructura

```
tools/
├── README.md
├── pyproject.toml
├── .gitignore
│
├── scripts/
│   ├── db-extract/              # Extrae datos de BD → CSV/XLSX
│   │   ├── extract.py           # Script principal (--db, --config)
│   │   ├── config.yaml          # Definición de tablas/campos
│   │   ├── db/                  # Capa de abstracción (MySQL, PG, SQLServer)
│   │   ├── pyproject.toml       # Dependencias aisladas
│   │   └── .env.example
│   │
│   ├── db-migrate/              # Migra datos entre BDs
│   │   ├── migrate.py           # Script principal (--source, --target, --mapping)
│   │   ├── mapping.yaml         # Relación campos fuente → destino
│   │   ├── db/                  # Capa de abstracción
│   │   ├── pyproject.toml
│   │   └── .env.example
│   │
│   └── repo-analyzer/           # Analiza repositorios Git
│       ├── analyze.py           # Script principal (--path, --repos, --days)
│       ├── output/              # Reportes y backups
│       ├── pyproject.toml
│       └── .env.example
```

## Inicio rápido

```bash
# Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ir al script que necesitás e instalar dependencias
cd scripts/db-extract
uv sync
uv run python extract.py --help
```

Cada script tiene su propio venv aislado — no hay conflictos entre dependencias.

## Scripts

| Script | Descripción | Ejemplo |
|---|---|---|
| `db-extract` | Extrae datos de BD a CSV/XLSX | `uv run python extract.py --db mysql` |
| `db-migrate` | Migra datos entre BDs con mapeo | `uv run python migrate.py --source mysql --target mysql` |
| `repo-analyzer` | Analiza repos Git, backup .env | `uv run python analyze.py --path /repos` |

## Capa de abstracción de BD

Los scripts `db-extract` y `db-migrate` comparten una arquitectura extensible:

| BD | Estado | Paquete |
|---|---|---|
| MySQL | Implementado | `pymysql` |
| PostgreSQL | Stub | `psycopg2` (próximamente) |
| SQL Server | Stub | `pyodbc` (próximamente) |

Para agregar una nueva BD, crear una clase en `db/` que implemente `DatabaseClient` (ver `db/base.py`).

## Variables sensibles

Cada script tiene su propio `.env` + `.env.example`. **Nunca commitear `.env`** (ya está en `.gitignore`).
