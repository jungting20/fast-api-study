# PostgreSQL DB Connection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Docker-based PostgreSQL and async DB connectivity to the FastAPI app.

**Architecture:** Use Docker Compose for local PostgreSQL. FastAPI reads `DATABASE_URL` from settings, creates an async SQLAlchemy engine/session in `app/db/session.py`, and exposes `/api/v1/health/db` for connection checks.

**Tech Stack:** Docker Compose, PostgreSQL 16, FastAPI, SQLAlchemy asyncio, asyncpg, pytest.

---

## File Structure

- Create `docker-compose.yml`: PostgreSQL service.
- Create `.env.example`: documented local env vars.
- Modify `pyproject.toml`: add `sqlalchemy[asyncio]` and `asyncpg`.
- Modify `app/core/config.py`: add `database_url`.
- Create `app/db/session.py`: async engine, session factory, dependency.
- Modify `app/api/v1/health.py`: add DB health endpoint.
- Modify `tests/test_main.py`: add DB health success and failure tests with dependency override.
- Modify `README.md`: document database startup and endpoint.

## Task 1: Add DB Health Contract

- [x] **Step 1: Write DB health tests**

Add tests for:

- `GET /api/v1/health/db` returns `{"status": "ok"}` when a fake session returns scalar `1`.
- `GET /api/v1/health/db` returns HTTP 503 when a fake session raises a SQLAlchemy error.

- [x] **Step 2: Run tests and verify failure**

Run:

```bash
uv run pytest
```

Expected: DB health tests fail before the endpoint exists.

- [x] **Step 3: Implement DB settings, session, and endpoint**

Add compose/env files, dependencies, settings, session dependency, and endpoint.

- [x] **Step 4: Run tests**

Run:

```bash
uv run pytest
```

Expected: all tests pass.

- [ ] **Step 5: Verify Docker PostgreSQL manually**

Run:

```bash
docker compose up -d postgres
uv run python -c "import asyncio; from sqlalchemy import text; from app.db.session import async_session_factory; async def main():\n    async with async_session_factory() as session:\n        result = await session.execute(text('SELECT 1'))\n        print(result.scalar_one())\nasyncio.run(main())"
```

Expected: prints `1`.
