# FastAPI uv Initial Setup Design

Date: 2026-06-21

## Scope

Create a small, production-friendly starting point for a FastAPI backend using `uv`.
The project should run locally, expose a basic health check, and include a focused
test that proves the app boots and responds.

## Architecture

The project will use a package-style layout:

- `app/main.py`: creates the FastAPI application and defines initial routes.
- `tests/test_main.py`: verifies the root and health endpoints.
- `pyproject.toml`: stores project metadata, runtime dependencies, dev
  dependencies, and pytest configuration.
- `README.md`: documents setup, run, and test commands.
- `.gitignore`: excludes virtual environments, caches, build outputs, and local
  environment files.

This keeps the initial structure simple while leaving room to add `app/api`,
`app/core`, `app/schemas`, or service modules later when real domain code exists.

## API Behavior

The initial app will provide:

- `GET /`: returns a small JSON message confirming the API is running.
- `GET /health`: returns a JSON health status.

No database, authentication, environment configuration, or external services are
included in the initial setup.

## Dependency Management

The project will use `uv` with:

- runtime dependencies: `fastapi`, `uvicorn`
- development dependencies: `pytest`, `httpx2`

The app can be run with `uv run uvicorn app.main:app --reload`.

## Testing

Tests will use FastAPI's test client to verify:

- `GET /` returns HTTP 200 and the expected JSON payload.
- `GET /health` returns HTTP 200 and the expected health payload.

The verification command will be `uv run pytest`.

## Error Handling

No custom error handling is needed for the initial setup. FastAPI's default
exception handling is sufficient until real API behavior is introduced.

## Out of Scope

- Database setup
- Authentication or authorization
- Docker configuration
- CI configuration
- Application settings management
- Logging customization
