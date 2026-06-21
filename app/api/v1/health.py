from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

router = APIRouter(tags=["health"])


def get_health_status() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health")
def health_check() -> dict[str, str]:
    return get_health_status()


@router.get("/health/db")
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

    return {"status": "ok"}
