from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.gemini import GeminiPlanInterpreter
from app.modules.plan_analysis.prompting import build_plan_extraction_prompt
from app.modules.plan_analysis.schemas import PlanAnalysisResponse
from app.modules.plan_analysis.service import (
    PlanAnalysisService,
    PlanNotFoundError,
)
from app.modules.upload.storage import MinioPlanStorage

router = APIRouter(
    prefix="/plan-analysis",
    tags=["Plan analysis"],
)


def get_plan_analysis_service(
    db: Session = Depends(get_db),
) -> PlanAnalysisService:
    return PlanAnalysisService(
        db=db,
        storage=MinioPlanStorage(),
        interpreter=GeminiPlanInterpreter(),
    )


@router.get("/extraction-contract")
def get_extraction_contract() -> dict[str, object]:
    return {
        "schema": PlanExtraction.model_json_schema(),
        "prompt": build_plan_extraction_prompt(),
    }


@router.post("/validate", response_model=PlanExtraction)
def validate_extraction(
    extraction: PlanExtraction,
) -> PlanExtraction:
    """Validate a provider's JSON before it reaches the business engine."""
    return extraction


@router.post(
    "/projects/{project_id}/plans/{plan_id}/analyse",
    response_model=PlanAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyse_plan(
    project_id: UUID,
    plan_id: UUID,
    service: PlanAnalysisService = Depends(get_plan_analysis_service),
) -> PlanAnalysisResponse:
    try:
        return service.analyse(
            project_id=project_id,
            plan_id=plan_id,
        )
    except PlanNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/projects/{project_id}/plans/{plan_id}/analyses",
    response_model=list[PlanAnalysisResponse],
)
def list_plan_analyses(
    project_id: UUID,
    plan_id: UUID,
    service: PlanAnalysisService = Depends(get_plan_analysis_service),
) -> list[PlanAnalysisResponse]:
    try:
        return service.list_analyses(project_id, plan_id)
    except PlanNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.get(
    "/projects/{project_id}/plans/{plan_id}/analyses/{analysis_id}",
    response_model=PlanAnalysisResponse,
)
def get_plan_analysis(
    project_id: UUID,
    plan_id: UUID,
    analysis_id: UUID,
    service: PlanAnalysisService = Depends(get_plan_analysis_service),
) -> PlanAnalysisResponse:
    try:
        return service.get_analysis(project_id, plan_id, analysis_id)
    except PlanNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
