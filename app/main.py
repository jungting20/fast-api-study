from fastapi import FastAPI

from app.api.router import router as api_router
from app.api.v1.health import get_health_status
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, debug=settings.debug)
    application.include_router(api_router)

    @application.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "FastAPI backend is running"}

    @application.get("/health", include_in_schema=False)
    def health_check() -> dict[str, str]:
        return get_health_status()

    return application


app = create_app()
