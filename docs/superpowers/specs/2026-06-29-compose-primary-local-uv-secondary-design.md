# Compose Primary Local uv Secondary Design

Date: 2026-06-29

## Scope

Make the project easy to run for personal study with two supported development
paths:

- Primary: run FastAPI and PostgreSQL together with Docker Compose.
- Secondary: run FastAPI on the host with `uv`, while PostgreSQL runs in
  Docker Compose.

The setup should stay small and understandable. It should not introduce
production deployment concerns.

## Architecture

The Docker Compose stack remains the default runtime:

- `web`: builds the local FastAPI image, mounts the project source, uses its own
  container virtual environment, exposes the API on the host, and waits for the
  PostgreSQL healthcheck.
- `postgres`: runs PostgreSQL 16 with a named volume for local data.

The host-local `uv` path reuses the same application code and dependencies, but
connects to PostgreSQL through `localhost`.

## Configuration

The `.env.example` file documents shared settings and the difference between
container and host database URLs:

- Compose injects a `DATABASE_URL` that points to the `postgres` service.
- Host-local `uv` execution uses `localhost` in `DATABASE_URL`.

The setup keeps local `.env` files ignored by git.

## Developer Commands

The README should make the main workflow explicit:

```bash
cp .env.example .env
docker compose up --build
docker compose exec web uv run alembic upgrade head
```

It should also document the secondary local workflow:

```bash
uv sync --dev
docker compose up -d postgres
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

A small `Makefile` may be added as a convenience layer for repeated study
commands, as long as it only wraps the documented commands and does not hide the
underlying tools.

## Error Handling

The README should include recovery commands for common local problems:

- stop services with `docker compose down`;
- reset disposable database state with `docker compose down -v`;
- rerun migrations with Alembic after recreating the database volume.

The application should continue to expose `/api/v1/health/db` for checking
database connectivity.

## Testing

Verification should cover:

- `uv run pytest` for application and configuration tests;
- `docker compose config` for Compose syntax and resolved configuration;
- full manual startup with `docker compose up --build` when Docker is available.

No new business behavior is required for this setup change.
