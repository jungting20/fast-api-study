from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

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


def test_api_v1_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_v1_database_health_check() -> None:
    from app.core.database import get_db_session

    class Result:
        def scalar_one(self) -> int:
            return 1

    class Session:
        async def execute(self, statement: object) -> Result:
            return Result()

    async def override_get_db_session() -> Session:
        yield Session()

    app.dependency_overrides[get_db_session] = override_get_db_session

    try:
        response = client.get("/api/v1/health/db")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_v1_database_health_check_returns_503_when_database_fails() -> None:
    from app.core.database import get_db_session

    class Session:
        async def execute(self, statement: object) -> None:
            raise SQLAlchemyError("connection failed")

    async def override_get_db_session() -> Session:
        yield Session()

    app.dependency_overrides[get_db_session] = override_get_db_session

    try:
        response = client.get("/api/v1/health/db")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
