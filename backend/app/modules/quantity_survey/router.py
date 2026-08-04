from fastapi import APIRouter

from app.modules.quantity_survey.schemas import QuantitySurveyRequest, QuantitySurveyResponse
from app.modules.quantity_survey.service import QuantitySurveyService

router = APIRouter(prefix="/quantity-surveys", tags=["Quantity surveys"])


@router.post("/calculate", response_model=QuantitySurveyResponse)
def calculate_quantity_survey(request: QuantitySurveyRequest) -> QuantitySurveyResponse:
    return QuantitySurveyService().calculate(request)
