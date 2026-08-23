# db-extract

Script para extraer datos de bases de datos a CSV o XLSX.

## Uso

```bash
# MySQL (por defecto)
uv run extract.py

# Especificar tipo de BD y config
uv run extract.py --db mysql --config config.yaml

# PostgreSQL (próximamente)
uv run extract.py --db postgres --config config.yaml
```

## Configuración

### Variables de entorno (`.env`)

| Variable | Descripción | Default |
|---|---|---|
| `DB_HOST` | Host de la BD | localhost |
| `DB_PORT` | Puerto | 3306 |
| `DB_NAME` | Nombre de la BD | - |
| `DB_USER` | Usuario | - |
| `DB_PASSWORD` | Contraseña | - |

### Configuración de extracción (`config.yaml`)

```yaml
extractions:
  - name: users_export          # Nombre descriptivo
    table: users                 # Tabla a consultar
    fields:                      # Campos a extraer (vacío = *)
      - id
      - name
      - email
    output_format: csv           # csv | xlsx
    output_file: output/users.csv
```

## Argumentos CLI

| Argumento | Opciones | Default | Descripción |
|---|---|---|---|
| `--db` | mysql, postgres, sqlserver | mysql | Tipo de BD |
| `--config` | ruta | config.yaml | Archivo de configuración |
