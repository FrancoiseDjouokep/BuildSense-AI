from fastapi import APIRouter

from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.prompting import build_plan_extraction_prompt

router = APIRouter(prefix="/plan-analysis", tags=["Plan analysis"])


@router.get("/extraction-contract")
def get_extraction_contract() -> dict[str, object]:
    return {
        "schema": PlanExtraction.model_json_schema(),
        "prompt": build_plan_extraction_prompt(),
    }


@router.post("/validate", response_model=PlanExtraction)
def validate_extraction(extraction: PlanExtraction) -> PlanExtraction:
    """Validate a provider's JSON before it is passed to the business engine."""
    return extraction
