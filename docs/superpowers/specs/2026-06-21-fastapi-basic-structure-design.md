# FastAPI Basic Structure Design

Date: 2026-06-21

## Scope

Restructure the starter FastAPI project into a conventional service layout while
preserving the existing root and health behavior.

## Architecture

The app will use separate package boundaries for application setup, API routing,
core configuration, and future domain layers:

- `app/main.py`: application factory and app instance.
- `app/api/router.py`: top-level API router registration.
- `app/api/v1/router.py`: versioned API router.
- `app/api/v1/health.py`: health endpoint.
- `app/core/config.py`: environment-backed application settings.
- `app/db`, `app/models`, `app/schemas`, `app/services`: package boundaries for
  future database, persistence, DTO, and business logic code.

Only `core/config.py` will contain real logic now. Other future-facing packages
will contain `__init__.py` files so imports have stable package locations without
adding unused abstractions.

## API Behavior

The existing endpoints remain available:

- `GET /`: returns `{"message": "FastAPI backend is running"}`.
- `GET /health`: returns `{"status": "ok"}`.

The versioned API also exposes:

- `GET /api/v1/health`: returns `{"status": "ok"}`.

## Dependency Management

Add `pydantic-settings` because Pydantic v2 moved `BaseSettings` into that
package. Existing FastAPI, Uvicorn, pytest, and HTTPX2 dependencies remain.

## Testing

Update endpoint tests to verify:

- The root endpoint still works.
- The legacy `/health` endpoint still works.
- The versioned `/api/v1/health` endpoint works.

The verification command remains `uv run pytest`.
