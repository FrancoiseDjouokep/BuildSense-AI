from typing import BinaryIO, Protocol

from app.core.config.settings import settings


class ObjectStorageError(Exception):
    """Raised when the object store cannot safely handle an upload."""


class ObjectStorageConfigurationError(ObjectStorageError):
    """Raised when credentials or bucket access are invalid."""


class PlanStorage(Protocol):
    def put(self, key: str, content: BinaryIO, size: int, mime_type: str) -> None: ...

    def delete(self, key: str) -> None: ...


class MinioPlanStorage:
    """Small S3-compatible adapter; MinIO is an implementation detail."""

    def __init__(self) -> None:
        try:
            import boto3
            from botocore.exceptions import ClientError
        except ImportError as error:
            raise RuntimeError(
                "Object-storage dependencies are missing. Run `uv sync --group dev`."
            ) from error

        self.bucket = settings.minio_bucket
        self.client_error_type = ClientError
        protocol = "https" if settings.minio_secure else "http"
        self.client = boto3.client(
            "s3",
            endpoint_url=f"{protocol}://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
        )

    def put(self, key: str, content: BinaryIO, size: int, mime_type: str) -> None:
        try:
            self._ensure_bucket()
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=content,
                ContentLength=size,
                ContentType=mime_type,
            )
        except self.client_error_type as error:
            raise ObjectStorageConfigurationError(
                "Unable to store the plan in object storage."
            ) from error

    def delete(self, key: str) -> None:
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
        except self.client_error_type as error:
            raise ObjectStorageError("Unable to remove a stored plan.") from error

    def _ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except self.client_error_type as error:
            code = error.response.get("Error", {}).get("Code")
            if code not in {"404", "NoSuchBucket"}:
                raise ObjectStorageConfigurationError(
                    "Object storage credentials or bucket permissions are invalid."
                ) from error
            try:
                self.client.create_bucket(Bucket=self.bucket)
            except self.client_error_type as create_error:
                raise ObjectStorageConfigurationError(
                    "Unable to create the plan storage bucket."
                ) from create_error
