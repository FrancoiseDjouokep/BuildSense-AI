from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.upload.models import PlanStatus


class PlanUploadResponse(BaseModel):
    id: UUID
    project_id: UUID
    original_filename: str
    mime_type: str
    size_bytes: int
    checksum: str
    status: PlanStatus
    is_duplicate: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
