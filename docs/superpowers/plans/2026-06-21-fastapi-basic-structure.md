# FastAPI Basic Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the starter FastAPI app into a conventional service layout.

**Architecture:** Keep `app/main.py` as the application entry point, move versioned endpoint routing under `app/api/v1`, and place app-wide settings in `app/core/config.py`. Preserve current endpoint behavior and add `/api/v1/health`.

**Tech Stack:** Python, uv, FastAPI, Uvicorn, pydantic-settings, pytest, HTTPX2.

---

## File Structure

- Modify `pyproject.toml`: add `pydantic-settings`.
- Modify `app/main.py`: use settings, app factory, and routers.
- Modify `tests/test_main.py`: add versioned health endpoint coverage.
- Create `app/api/__init__.py`: API package marker.
- Create `app/api/router.py`: top-level API router.
- Create `app/api/v1/__init__.py`: v1 package marker.
- Create `app/api/v1/router.py`: v1 router aggregation.
- Create `app/api/v1/health.py`: health endpoint router and payload helper.
- Create `app/core/__init__.py`: core package marker.
- Create `app/core/config.py`: settings object.
- Create `app/db/__init__.py`, `app/models/__init__.py`, `app/schemas/__init__.py`, `app/services/__init__.py`: future package boundaries.

## Task 1: Add Versioned API Structure

- [x] **Step 1: Add a failing test for `/api/v1/health`**

Expected test addition:

```python
def test_api_v1_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [x] **Step 2: Run tests and verify the new test fails**

Run:

```bash
uv run pytest
```

Expected: `/api/v1/health` returns 404 before router implementation.

- [x] **Step 3: Implement settings and routers**

Create the API and core package files, update `app/main.py`, and add
`pydantic-settings` to `pyproject.toml`.

- [x] **Step 4: Run verification**

Run:

```bash
uv run pytest
```

Expected: all endpoint tests pass.

- [x] **Step 5: Verify server response**

Run while the server is active:

```bash
curl -sS http://127.0.0.1:8000/api/v1/health
```

Expected:

```json
{"status":"ok"}
```
