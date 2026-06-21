# Backend

FastAPI backend starter managed with `uv`.

## Requirements

- Python 3.12+
- uv

## Setup

```bash
uv sync --dev
```

## Database

Start PostgreSQL:

```bash
docker compose up -d postgres
```

The local connection URL is:

```text
postgresql+asyncpg://backend:backend@localhost:5432/backend
```

Create a local `.env` from the example if you want to override defaults:

```bash
cp .env.example .env
```

Stop PostgreSQL:

```bash
docker compose down
```

Stop PostgreSQL and delete local database data:

```bash
docker compose down -v
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Structure

```text
app/
  api/
    router.py
    v1/
      health.py
      router.py
  core/
    config.py
  db/
  models/
  schemas/
  services/
  main.py
```

## Endpoints

- `GET /`
- `GET /health`
- `GET /api/v1/health`
- `GET /api/v1/health/db`

## Test

```bash
uv run pytest
```
