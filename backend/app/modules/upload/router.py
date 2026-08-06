from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.upload.schemas import PlanResponse, PlanUploadResponse
from app.modules.upload.service import UploadService
from app.modules.upload.storage import MinioPlanStorage

router = APIRouter(prefix="/projects/{project_id}/plans", tags=["Plans"])


def get_upload_service(db: Session = Depends(get_db)) -> UploadService:
    return UploadService(db=db, storage=MinioPlanStorage())


@router.get("", response_model=list[PlanResponse])
def list_project_plans(
    project_id: UUID,
    include_archived: bool = Query(default=False),
    service: UploadService = Depends(get_upload_service),
) -> list[PlanResponse]:
    return service.list_plans(project_id, include_archived=include_archived)


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(
    project_id: UUID,
    plan_id: UUID,
    service: UploadService = Depends(get_upload_service),
) -> PlanResponse:
    return service.get_plan(project_id, plan_id)


@router.post("/{plan_id}/archive", response_model=PlanResponse)
def archive_plan(
    project_id: UUID,
    plan_id: UUID,
    service: UploadService = Depends(get_upload_service),
) -> PlanResponse:
    return service.archive_plan(project_id, plan_id)


@router.post("", response_model=PlanUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_plan(
    project_id: UUID,
    file: UploadFile = File(...),
    service: UploadService = Depends(get_upload_service),
) -> PlanUploadResponse:
    return await service.upload(project_id, file)
