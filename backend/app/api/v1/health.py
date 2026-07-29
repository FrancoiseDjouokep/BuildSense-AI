from fastapi import APIRouter

from app.core.config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }