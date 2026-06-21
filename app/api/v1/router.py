from fastapi import APIRouter

from app.api.v1 import health
from app.api.v1.qna import qna

router = APIRouter()
router.include_router(health.router)
router.include_router(qna.router, prefix="/qna")
