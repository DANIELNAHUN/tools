# db-migrate

Script para migrar datos entre bases de datos con mapeo configurable de campos.

## Uso

```bash
# MySQL -> MySQL (default)
uv run migrate.py

# Especificar origen y destino
uv run migrate.py --source mysql --target mysql --mapping mapping.yaml

# Cross-database (próximamente)
uv run migrate.py --source mysql --target postgres
```

## Configuración

### Variables de entorno (`.env`)

| Variable | Descripción | Default |
|---|---|---|
| `SOURCE_DB_HOST` | Host de la BD origen | localhost |
| `SOURCE_DB_PORT` | Puerto origen | 3306 |
| `SOURCE_DB_NAME` | BD origen | - |
| `SOURCE_DB_USER` | Usuario origen | - |
| `SOURCE_DB_PASSWORD` | Contraseña origen | - |
| `TARGET_DB_HOST` | Host de la BD destino | localhost |
| `TARGET_DB_PORT` | Puerto destino | 3306 |
| `TARGET_DB_NAME` | BD destino | - |
| `TARGET_DB_USER` | Usuario destino | - |
| `TARGET_DB_PASSWORD` | Contraseña destino | - |

### Mapeo de campos (`mapping.yaml`)

```yaml
migrations:
  - name: users_migration
    source_table: users
    target_table: users_v2
    field_mapping:
      id: id
      name: full_name          # renombrado
      email: email
```

## Argumentos CLI

| Argumento | Opciones | Default | Descripción |
|---|---|---|---|
| `--source` | mysql, postgres, sqlserver | mysql | Tipo de BD origen |
| `--target` | mysql, postgres, sqlserver | mysql | Tipo de BD destino |
| `--mapping` | ruta | mapping.yaml | Archivo de mapeo |
