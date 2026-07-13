"""
Database clients for BankGuard Enterprise.

PostgreSQL stores core banking records. MongoDB is optional and intended for
raw telemetry such as login events, device fingerprints, and audit payloads.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings

try:
    from pymongo import MongoClient
    from pymongo.database import Database as MongoDatabase
except ImportError:
    MongoClient = None
    MongoDatabase = None


def _sync_database_url(url: str) -> str:
    """Convert async SQLAlchemy URLs to a sync driver URL for this prototype."""
    return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)


engine: Engine = create_engine(
    _sync_database_url(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
      yield session
    finally:
      session.close()


def check_postgres() -> bool:
    with engine.connect() as connection:
        connection.execute(text("select 1"))
    return True


def get_mongo_database() -> Optional["MongoDatabase"]:
    if not settings.MONGODB_URI or MongoClient is None:
        return None

    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=3000)
    return client[settings.MONGODB_DATABASE]


def check_mongo() -> bool:
    database = get_mongo_database()
    if database is None:
        return False

    database.command("ping")
    return True
