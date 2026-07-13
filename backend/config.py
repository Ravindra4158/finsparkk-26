"""
BankGuard Enterprise — Application Configuration.

Centralises all environment-driven settings via Pydantic Settings.
Defaults are tuned for local development; override with env vars or a .env
file in production.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "BankGuard Enterprise API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_flag(cls, value):
        if isinstance(value, str) and value.lower() in {"release", "prod", "production"}:
            return False
        return value

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://bankguard:bankguard@localhost:5432/bankguard"

    # ── MongoDB (optional raw telemetry / event store) ───────────────────
    MONGODB_URI: str = ""
    MONGODB_DATABASE: str = "bankguard"

    # ── Redis ────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Neo4j (Graph) ────────────────────────────────────────────────────
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "bankguard_dev"

    # ── JWT / Auth ───────────────────────────────────────────────────────
    JWT_SECRET: str = "super-secret-change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── External APIs ────────────────────────────────────────────────────
    SWIFT_API_URL: str = "http://localhost:8081/swift"
    CBS_API_URL: str = "http://localhost:8082/cbs"

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]

    # ── ML Model Paths ───────────────────────────────────────────────────
    UEBA_MODEL_PATH: str = str(Path("ml/models/ueba_isolation_forest.pkl"))
    LOAN_MODEL_PATH: str = str(Path("ml/models/loan_xgboost.json"))
    NLP_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # ── Celery ───────────────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"


settings = Settings()
