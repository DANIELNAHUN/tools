# repo-analyzer

Script para analizar repositorios Git en un directorio: estado, cambios locales y backup de `.env`.

## Uso

```bash
# Analizar todos los repos en el directorio actual
uv run analyze.py

# Directorio específico
uv run analyze.py --path /home/user/projects

# Filtrar repos específicos
uv run analyze.py --repos repo1,repo2

# Combinar: directorio + filtro
uv run analyze.py --path /home/user/projects --repos repo1,repo2

# Cambiar ventana de actividad (default: 30 días)
uv run analyze.py --days 60
```

## Qué analiza

| Check | Descripción |
|---|---|
| **Activo/Inactivo** | Commits en los últimos N días |
| **Cambios locales** | Archivos modificados sin commit |
| **Sin subir** | Commits locales sin push al remote |
| **Backup .env** | Copia todos los `.env` a un zip |
| **Remote URL** | URL del repositorio remoto |

## Configuración

### Variables de entorno (`.env`)

| Variable | Descripción | Default |
|---|---|---|
| `GITHUB_TOKEN` | Token para API GitHub (opcional) | - |
| `OUTPUT_DIR` | Directorio de salida | output |

## Argumentos CLI

| Argumento | Default | Descripción |
|---|---|---|
| `--path` | Directorio actual | Directorio con repos |
| `--repos` | Todos | Filtrar por nombres (comma-separated) |
| `--days` | 30 | Días para considerar "activo" |
