"""Application configuration using Pydantic settings."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    SECRET_KEY: str
    SESSION_TIMEOUT_MINUTES: int = Field(default=15, ge=1)
    BCRYPT_ROUNDS: int = Field(default=12, ge=4)
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    APP_NAME: str = "CareLink"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
