from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.project.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.modules.project.service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def get_project_service(
    db: Session = Depends(get_db),
) -> ProjectService:
    return ProjectService(db)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    return service.create(data)


@router.get(
    "/",
    response_model=list[ProjectResponse],
)
def list_projects(
    service: ProjectService = Depends(get_project_service),
):
    return service.list()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    return service.get(project_id)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    return service.update(project_id, data)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    service.delete(project_id)