from fastapi import APIRouter

router = APIRouter(tags=["qna"])


def get_health_status() -> dict[str, str]:
    return {"status": "qna"}


@router.get("/test")
def health_check() -> dict[str, str]:
    return get_health_status()
