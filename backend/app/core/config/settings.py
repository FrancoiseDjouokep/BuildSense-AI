from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()