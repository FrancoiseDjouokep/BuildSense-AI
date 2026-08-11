from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.models import AnalysisStatus


class PlanAnalysisResponse(BaseModel):
    id: UUID
    plan_id: UUID
    status: AnalysisStatus
    provider: str
    model: str
    prompt_version: str
    result: PlanExtraction | None
    error_message: str | None
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
