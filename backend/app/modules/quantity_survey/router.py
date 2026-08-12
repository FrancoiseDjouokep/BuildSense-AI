from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database.session import get_db  # ⚠️ ajuste le nom si ta dépendance s'appelle autrement
from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.models import AnalysisStatus, PlanAnalysis
from app.modules.quantity_survey.schemas import QuantitySurveyRequest, QuantitySurveyResponse
from app.modules.quantity_survey.service import QuantitySurveyService

router = APIRouter(prefix="/quantity-surveys", tags=["Quantity surveys"])


@router.post("/calculate", response_model=QuantitySurveyResponse)
def calculate_quantity_survey(request: QuantitySurveyRequest) -> QuantitySurveyResponse:
    return QuantitySurveyService().calculate(request)


@router.get("/by-plan/{plan_id}", response_model=QuantitySurveyResponse)
def get_quantity_survey_for_plan(plan_id: UUID, db: Session = Depends(get_db)) -> QuantitySurveyResponse:
    analysis = (
        db.query(PlanAnalysis)
        .filter(
            PlanAnalysis.plan_id == plan_id,
            PlanAnalysis.status == AnalysisStatus.completed,  # ⚠️ ajuste au nom exact du membre enum
        )
        .order_by(PlanAnalysis.completed_at.desc())
        .first()
    )

    if analysis is None or analysis.result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No completed plan analysis found for this plan",
        )

    extraction = PlanExtraction.model_validate(analysis.result)
    return QuantitySurveyService().calculate_from_extraction(extraction)