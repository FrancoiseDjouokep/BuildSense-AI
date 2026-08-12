from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.modules.plan_analysis.router import router as plan_analysis_router
from app.modules.project.router import router as project_router
from app.modules.quantity_survey.router import router as quantity_survey_router
from app.modules.upload.router import router as upload_router
from app.modules.pricing.router import router as pricing_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(project_router)
api_router.include_router(plan_analysis_router)
api_router.include_router(quantity_survey_router)
api_router.include_router(upload_router)
api_router.include_router(pricing_router)

