from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.project.models import Project
from app.modules.project.schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())

        self.db.add(project)

        return project

    def get_by_id(self, project_id: UUID) -> Project | None:
        statement = select(Project).where(Project.id == project_id)

        return self.db.scalar(statement)

    def list(self) -> list[Project]:
        statement = select(Project).order_by(Project.created_at.desc())

        return list(self.db.scalars(statement).all())

    def update(
        self,
        project: Project,
        data: ProjectUpdate,
    ) -> Project:

        values = data.model_dump(exclude_unset=True)

        for field, value in values.items():
            setattr(project, field, value)


        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)