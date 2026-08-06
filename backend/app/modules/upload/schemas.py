from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.upload.models import PlanStatus


class PlanResponse(BaseModel):
    id: UUID
    project_id: UUID
    original_filename: str
    mime_type: str
    size_bytes: int
    checksum: str
    status: PlanStatus
    created_at: datetime
    archived_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class PlanUploadResponse(PlanResponse):
    is_duplicate: bool = False
