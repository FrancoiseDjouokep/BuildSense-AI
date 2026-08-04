from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.upload.schemas import PlanUploadResponse
from app.modules.upload.service import UploadService
from app.modules.upload.storage import MinioPlanStorage

router = APIRouter(prefix="/projects/{project_id}/plans", tags=["Plans"])


def get_upload_service(db: Session = Depends(get_db)) -> UploadService:
    return UploadService(db=db, storage=MinioPlanStorage())


@router.post("", response_model=PlanUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_plan(
    project_id: UUID,
    file: UploadFile = File(...),
    service: UploadService = Depends(get_upload_service),
) -> PlanUploadResponse:
    return await service.upload(project_id, file)
