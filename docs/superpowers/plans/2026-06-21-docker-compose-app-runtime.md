# Docker Compose App Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run FastAPI and PostgreSQL together with `docker compose up --build`.

**Architecture:** Add a Python/uv Docker image for the FastAPI app and extend Compose with a `web` service. Use a bind mount for live source reload and a named `.venv` volume so the container does not reuse the host virtual environment. Sync runtime dependencies only inside the app container.

**Tech Stack:** Docker, Docker Compose, Python 3.12, uv, FastAPI, PostgreSQL 16.

---

## File Structure

- Create `Dockerfile`: FastAPI app image using uv and Python 3.12.
- Create `.dockerignore`: exclude host-only files from image builds.
- Modify `docker-compose.yml`: add `web`, preserve `postgres`, add `web_venv`.
- Modify `.env.example`: keep host-local DB URL and add app port defaults.
- Modify `README.md`: make Compose the primary startup path.

## Task 1: Add Docker App Runtime

- [x] **Step 1: Create Dockerfile**

Create a uv-based Python image that installs project dependencies and runs from
`/app`.

- [x] **Step 2: Add .dockerignore**

Exclude `.venv`, Git metadata, caches, and local env files from image context.

- [x] **Step 3: Extend docker-compose.yml**

Add a `web` service with:

- `build: .`
- `ports: "8000:8000"`
- `volumes: .:/app` and `web_venv:/app/.venv`
- `DATABASE_URL` pointing at `postgres`
- `depends_on.postgres.condition: service_healthy`

- [x] **Step 4: Update README and .env.example**

Document `docker compose up --build` as the primary run command and keep local
non-Docker commands available as alternatives.

- [x] **Step 5: Verify application tests**

Run:

```bash
uv run pytest
```

Expected: all tests pass.

- [x] **Step 6: Verify Compose config**

Run:

```bash
docker compose config
```

Expected: Compose renders `web`, `postgres`, `postgres_data`, and `web_venv`.

- [x] **Step 7: Attempt full stack startup when Docker daemon is available**

Run:

```bash
docker compose up --build
```

Expected with Docker daemon running: FastAPI starts on `http://127.0.0.1:8000`
and `/api/v1/health/db` returns `{"status":"ok"}`.
