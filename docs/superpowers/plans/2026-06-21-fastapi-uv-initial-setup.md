# FastAPI uv Initial Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a runnable FastAPI starter backend managed by `uv`.

**Architecture:** Use a package-style `app` directory with a single `main.py` entry point. Keep the first API surface intentionally small with root and health endpoints, and verify both through pytest using FastAPI's test client.

**Tech Stack:** Python, uv, FastAPI, Uvicorn, pytest, HTTPX2.

---

## File Structure

- Create `pyproject.toml`: project metadata, dependencies, dev dependencies, and pytest config.
- Create `.gitignore`: Python, uv, editor, and local environment exclusions.
- Create `README.md`: setup, run, and test commands.
- Create `app/__init__.py`: marks `app` as a package.
- Create `app/main.py`: FastAPI application and initial endpoints.
- Create `tests/test_main.py`: endpoint tests.

## Task 1: Scaffold FastAPI uv Project

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `tests/test_main.py`

- [x] **Step 1: Write the endpoint tests first**

Create `tests/test_main.py`:

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI backend is running"}


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [x] **Step 2: Run tests to verify they fail before implementation**

Run:

```bash
uv run pytest
```

Expected before dependencies and app files exist: failure because the test module or dependencies cannot import `fastapi` or `app.main`.

- [x] **Step 3: Create project metadata and dependencies**

Create `pyproject.toml`:

```toml
[project]
name = "backend"
version = "0.1.0"
description = "FastAPI backend starter"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
]

[dependency-groups]
dev = [
    "httpx2>=0.28.0",
    "pytest>=8.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- [x] **Step 4: Create the FastAPI app**

Create `app/__init__.py`:

```python
```

Create `app/main.py`:

```python
from fastapi import FastAPI


app = FastAPI(title="Backend API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI backend is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

- [x] **Step 5: Add standard local ignores**

Create `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.env
.env.*
!.env.example
.DS_Store
```

- [x] **Step 6: Document usage**

Create `README.md`:

```markdown
# Backend

FastAPI backend starter managed with `uv`.

## Requirements

- Python 3.12+
- uv

## Setup

```bash
uv sync --dev
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Test

```bash
uv run pytest
```
```

- [x] **Step 7: Run verification**

Run:

```bash
uv run pytest
```

Expected: both endpoint tests pass.

- [x] **Step 8: Optionally start the local server**

Run:

```bash
uv run uvicorn app.main:app --reload
```

Expected: Uvicorn starts successfully and serves the API at `http://127.0.0.1:8000`.

- [ ] **Step 9: Commit if this directory has been initialized as a Git repository**

Run only if `git status --short` succeeds:

```bash
git add .gitignore README.md pyproject.toml app tests docs/superpowers
git commit -m "chore: initialize fastapi uv backend"
```

Expected in the current directory: commit only if the user explicitly asks for a commit.

## Self-Review

- Spec coverage: the plan creates the app package, FastAPI endpoints, uv dependency metadata, README, .gitignore, and pytest coverage required by the design.
- Placeholder scan: no TBD, TODO, or unspecified implementation steps remain.
- Type consistency: endpoint names and response payloads match the tests exactly.
