# Docker Compose App Runtime Design

Date: 2026-06-21

## Scope

Run the FastAPI app and PostgreSQL together with one Docker Compose command for
local development.

## Architecture

The Compose stack will contain:

- `web`: builds the FastAPI image from the local `Dockerfile`, runs Uvicorn with
  reload enabled, publishes port `8000`, and depends on PostgreSQL health.
- `postgres`: runs PostgreSQL 16, publishes port `5432`, and stores data in a
  named volume.

The `web` service mounts the project source into `/app` for live reload. It also
mounts a named volume at `/app/.venv` so the Linux container keeps its own
virtual environment instead of using the host `.venv`.
The container syncs only runtime dependencies before starting Uvicorn.

## Configuration

Inside Compose, the app connects to PostgreSQL through the service DNS name:

```text
postgresql+asyncpg://backend:backend@postgres:5432/backend
```

For local host execution outside Docker, `.env.example` still documents a
`localhost` database URL.

## Commands

The primary local startup command becomes:

```bash
docker compose up --build
```

The app remains available at `http://127.0.0.1:8000`.

## Verification

- `uv run pytest` verifies application behavior outside Docker.
- `docker compose config` verifies Compose syntax and service wiring without
  requiring a running Docker daemon.
- `docker compose up --build` verifies the full stack when Docker daemon is
  available.
