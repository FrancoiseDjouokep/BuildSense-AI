"""Prompt construction for vision models. The response is validated separately."""

import json

from app.modules.plan_analysis.contracts import PlanExtraction

PLAN_EXTRACTION_PROMPT_VERSION = "v1"


def build_plan_extraction_prompt() -> str:
    """Return a provider-neutral instruction that asks for observations, never maths."""
    schema = json.dumps(PlanExtraction.model_json_schema(), ensure_ascii=False)
    return (
        "You are an architectural-plan interpreter. Inspect the attached 2D plan. "
        "Return only one JSON object conforming to this JSON Schema: "
        f"{schema}. "
        "Use metres for every dimension. Extract values explicitly shown or reliably "
        "inferred from the plan scale. Do not calculate areas, volumes, quantities, "
        "prices, estimates, or add prose. If an element is not reliable, omit it."
    )
