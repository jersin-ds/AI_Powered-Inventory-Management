"""Application configuration loaded from environment variables."""

from __future__ import annotations

import json
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite:///./inventory.db"

    # JWT
    jwt_secret: str = "super-secret-inventory-jwt-key-2024"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 1440  # 24 hours

    # Cerebras AI
    cerebras_api_key: str = ""
    cerebras_model: str = "llama3.1-8b"

    # CORS
    cors_origins: str = '["http://localhost:5173","http://localhost:3000"]'

    @property
    def cors_origin_list(self) -> list[str]:
        try:
            return json.loads(self.cors_origins)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:5173"]


settings = Settings()
