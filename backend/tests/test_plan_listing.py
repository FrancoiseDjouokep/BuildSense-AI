from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.modules.project.models import Project
from app.modules.upload.models import Plan, PlanStatus
from app.modules.upload.service import UploadService


def make_plan(project_id: object, filename: str) -> Plan:
    return Plan(
        id=uuid4(),
        project_id=project_id,
        original_filename=filename,
        storage_key=f"plans/{filename}",
        mime_type="application/pdf",
        size_bytes=1024,
        checksum="a" * 64,
        status=PlanStatus.UPLOADED,
        created_at=datetime.now(UTC),
    )


def test_lists_project_plans() -> None:
    project = Project(id=uuid4(), name="Maison témoin")
    first_plan = make_plan(project.id, "ground-floor.pdf")
    second_plan = make_plan(project.id, "first-floor.pdf")
    db = MagicMock()
    db.get.return_value = project
    db.scalars.return_value.all.return_value = [second_plan, first_plan]
    service = UploadService(db=db, storage=MagicMock())

    result = service.list_plans(project.id)

    assert [plan.original_filename for plan in result] == [
        "first-floor.pdf",
        "ground-floor.pdf",
    ]
    assert all(plan.status == PlanStatus.UPLOADED for plan in result)


def test_rejects_listing_for_unknown_project() -> None:
    db = MagicMock()
    db.get.return_value = None
    service = UploadService(db=db, storage=MagicMock())

    with pytest.raises(HTTPException, match="Project not found"):
        service.list_plans(uuid4())
