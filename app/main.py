from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db_session
from app.qna.router import router as qna_router


def get_health_status() -> dict[str, str]:
    return {"status": "ok"}


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, debug=settings.debug)
    application.include_router(qna_router, prefix=f"{settings.api_v1_prefix}/qna")

    @application.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "FastAPI backend is running"}

    @application.get("/health", include_in_schema=False)
    def health_check() -> dict[str, str]:
        return get_health_status()

    @application.get(f"{settings.api_v1_prefix}/health")
    def api_health_check() -> dict[str, str]:
        return get_health_status()

    @application.get(f"{settings.api_v1_prefix}/health/db")
    async def database_health_check(
        session: AsyncSession = Depends(get_db_session),
    ) -> dict[str, str]:
        try:
            result = await session.execute(text("SELECT 1"))
            result.scalar_one()
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            ) from exc

        return get_health_status()

    return application


app = create_app()
