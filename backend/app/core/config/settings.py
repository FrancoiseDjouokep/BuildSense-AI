from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================================================================
    # Application
    # =========================================================================
    app_name: str = "BuildSense AI"
    app_version: str = "0.1.0"

    app_env: Literal[
        "development",
        "test",
        "staging",
        "production",
    ] = "development"

    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # =========================================================================
    # Database
    # =========================================================================
    database_host: str = "localhost"
    database_port: int = 5435
    database_name: str = "buildsense"
    database_user: str = "postgres"
    database_password: str = "postgres"

    # =========================================================================
    # Object storage (MinIO / S3)
    # =========================================================================
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "buildsense-plans"
    minio_secure: bool = False

    # =========================================================================
    # LLM
    # =========================================================================
    llm_provider: str = "gemini"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-2.5-flash"

    # =========================================================================
    # Configuration
    # =========================================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )


settings = Settings()
