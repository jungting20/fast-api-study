# Backend

FastAPI backend starter managed with `uv`.

## Requirements

- Docker
- Docker Compose

## Run With Docker Compose

```bash
docker compose up --build
```

The API will be available at `http://127.0.0.1:8000`.

Create a local `.env` from the example if you want to override defaults:

```bash
cp .env.example .env
```

Stop the stack:

```bash
docker compose down
```

Stop the stack and delete local database data:

```bash
docker compose down -v
```

## Local Python Run

Use this only if you want to run FastAPI on the host instead of inside Docker.

```bash
uv sync --dev
docker compose up -d postgres
uv run uvicorn app.main:app --reload
```

The host-local database URL is:

```text
postgresql+asyncpg://backend:backend@localhost:5432/backend
```

## Database Migrations

This project uses Alembic for schema migrations. Migrations are run manually;
the API process does not create or upgrade tables on startup.

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Apply all migrations:

```bash
uv run alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe schema change"
```

Review the generated file in `alembic/versions/`, then apply it:

```bash
uv run alembic upgrade head
```

Rollback the latest migration:

```bash
uv run alembic downgrade -1
```

If a local development database was initialized with different credentials,
PostgreSQL may reject the default `backend` role. For disposable local data,
recreate the volume and run migrations again:

```bash
docker compose down -v
docker compose up -d postgres
uv run alembic upgrade head
```

## Structure

```text
.
  Dockerfile
  docker-compose.yml
  alembic.ini
  alembic/
  app/
    api/
      router.py
      v1/
        health.py
        router.py
    core/
      config.py
    db/
      session.py
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
