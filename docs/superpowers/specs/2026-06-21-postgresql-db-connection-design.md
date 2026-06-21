# PostgreSQL DB Connection Design

Date: 2026-06-21

## Scope

Add local PostgreSQL support for development and wire FastAPI to the database
through an async SQLAlchemy session. The initial DB-facing API surface is a
versioned health endpoint that confirms the app can execute a simple query.

## Architecture

- `docker-compose.yml`: runs PostgreSQL 16 with a named volume.
- `.env.example`: documents local database environment values.
- `app/core/config.py`: exposes `database_url`.
- `app/db/session.py`: owns the async SQLAlchemy engine, session factory, and
  FastAPI dependency.
- `app/api/v1/health.py`: adds `GET /health/db`, which executes `SELECT 1`.

The top-level router already applies `/api/v1`, so the final DB health URL is
`GET /api/v1/health/db`.

## Dependencies

Add:

- `sqlalchemy[asyncio]`
- `asyncpg`

Alembic is intentionally out of scope until the first real table/model exists.

## Error Handling

If the database query fails, the DB health endpoint returns HTTP 503 with
`{"detail": "Database unavailable"}`.

## Testing

Tests will override the DB session dependency with fake async sessions so the
unit test suite does not require Docker. Docker is used for manual integration
verification after the code passes.
