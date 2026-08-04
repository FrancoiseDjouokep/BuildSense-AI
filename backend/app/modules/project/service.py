from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.project.repository import ProjectRepository
from app.modules.project.schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProjectRepository(db)

    def create(self, data: ProjectCreate):
        try:
            project = self.repository.create(data)

            self.db.commit()
            self.db.refresh(project)

            return project

        except Exception:
            self.db.rollback()
            raise

    def get(self, project_id: UUID):
        project = self.repository.get_by_id(project_id)

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    def list(self):
        return self.repository.list()

    def update(
        self,
        project_id: UUID,
        data: ProjectUpdate,
    ):
        project = self.get(project_id)

        try:
            project = self.repository.update(project, data)

            self.db.commit()
            self.db.refresh(project)

            return project

        except Exception:
            self.db.rollback()
            raise

    def delete(self, project_id: UUID):
        project = self.get(project_id)

        try:
            self.repository.delete(project)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise