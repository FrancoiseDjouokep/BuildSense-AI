from fastapi import FastAPI

from app.core.config.settings import settings
from app.api.router import api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description="AI-powered quantity surveying platform.",
    )

    app.include_router(api_router)

    return app