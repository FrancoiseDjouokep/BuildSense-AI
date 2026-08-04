import hashlib
import logging
import re
from tempfile import SpooledTemporaryFile
from typing import BinaryIO
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.project.models import Project
from app.modules.upload.models import Plan
from app.modules.upload.schemas import PlanResponse, PlanUploadResponse
from app.modules.upload.storage import ObjectStorageError, PlanStorage

logger = logging.getLogger(__name__)

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
READ_CHUNK_BYTES = 1024 * 1024
ALLOWED_MIME_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}


def detect_mime_type(header: bytes) -> str | None:
    if header.startswith(b"%PDF-"):
        return "application/pdf"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if header.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if header.startswith((b"II*\x00", b"MM\x00*")):
        return "image/tiff"
    return None


def validate_filename_and_content(filename: str, header: bytes) -> str:
    suffix = "." + filename.rsplit(".", maxsplit=1)[-1].lower() if "." in filename else ""
    expected_mime_type = ALLOWED_MIME_TYPES.get(suffix)
    if expected_mime_type is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file extension. Allowed: PDF, PNG, JPG, TIFF.",
        )
    detected_mime_type = detect_mime_type(header)
    if detected_mime_type != expected_mime_type:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File content does not match its extension.",
        )
    return detected_mime_type


def build_storage_key(project_id: UUID, filename: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename).strip("._") or "plan"
    return f"plans/{project_id}/{uuid4()}_{safe_name}"


class UploadService:
    def __init__(self, db: Session, storage: PlanStorage):
        self.db = db
        self.storage = storage

    async def upload(self, project_id: UUID, upload: UploadFile) -> PlanUploadResponse:
        self._get_project(project_id)
        filename = upload.filename or ""
        content, size, checksum, mime_type = await self._read_and_validate(upload, filename)
        is_duplicate = self._is_duplicate(project_id, checksum)
        storage_key = build_storage_key(project_id, filename)
        stored = False

        try:
            self.storage.put(storage_key, content, size, mime_type)
            stored = True
            plan = Plan(
                project_id=project_id,
                original_filename=filename,
                storage_key=storage_key,
                mime_type=mime_type,
                size_bytes=size,
                checksum=checksum,
            )
            self.db.add(plan)
            self.db.commit()
            self.db.refresh(plan)
        except ObjectStorageError as error:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Plan storage is temporarily unavailable.",
            ) from error
        except Exception:
            self.db.rollback()
            if stored:
                try:
                    self.storage.delete(storage_key)
                except ObjectStorageError:
                    # Preserve the database error; failed cleanup is recoverable.
                    logger.warning("Unable to clean up stored plan %s", storage_key)
            raise
        finally:
            content.close()
            await upload.close()

        return PlanUploadResponse.model_validate(plan).model_copy(
            update={"is_duplicate": is_duplicate}
        )

    def list_plans(self, project_id: UUID) -> list[PlanResponse]:
        self._get_project(project_id)
        statement = (
            select(Plan)
            .where(Plan.project_id == project_id)
            .order_by(Plan.created_at.desc())
        )
        plans = self.db.scalars(statement).all()
        return [PlanResponse.model_validate(plan) for plan in plans]

    def _get_project(self, project_id: UUID) -> Project:
        project = self.db.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    def _is_duplicate(self, project_id: UUID, checksum: str) -> bool:
        statement = select(Plan.id).where(
            Plan.project_id == project_id,
            Plan.checksum == checksum,
        )
        return self.db.scalar(statement) is not None

    async def _read_and_validate(
        self, upload: UploadFile, filename: str
    ) -> tuple[BinaryIO, int, str, str]:
        # The caller owns and closes this stream after MinIO has consumed it.
        content = SpooledTemporaryFile(  # noqa: SIM115
            max_size=5 * 1024 * 1024,
            mode="w+b",
        )
        digest = hashlib.sha256()
        size = 0
        header = b""
        try:
            while chunk := await upload.read(READ_CHUNK_BYTES):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="File exceeds the 50 MB upload limit.",
                    )
                if len(header) < 32:
                    header += chunk[: 32 - len(header)]
                digest.update(chunk)
                content.write(chunk)
            mime_type = validate_filename_and_content(filename, header)
            content.seek(0)
            return content, size, digest.hexdigest(), mime_type
        except Exception:
            content.close()
            await upload.close()
            raise
