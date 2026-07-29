from fastapi import FastAPI

from app.core.config.settings import settings


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

    @app.get("/", tags=["Health"])
    async def root():
        return {
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
            "status": "running",
        }

    return app