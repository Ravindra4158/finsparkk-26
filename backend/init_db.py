"""
Database Initialization Script.

Creates all tables from models and sets up the schema.
Run this once at startup or during deployment.

Usage:
    python init_db.py
"""

import logging
from sqlalchemy import text

from config import settings
from db import engine
from models.database import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_database():
    """
    Initialize the database schema.
    
    - Creates all tables from SQLAlchemy models
    - Creates indexes for performance
    - Sets up extensions (for PostgreSQL)
    """
    logger.info("Starting database initialization...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✓ All tables created successfully")

        # Create useful indexes
        with engine.connect() as connection:
            # Index on employee expiration for cleanup queries
            connection.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_employee_expires_at 
                    ON employees(expires_at) 
                    WHERE expires_at IS NOT NULL
                    """
                )
            )
            logger.info("✓ Created index on employees.expires_at")

            # Index on behavior log timestamps for time-series queries
            connection.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_behavior_log_timestamp 
                    ON behavior_logs(timestamp DESC)
                    """
                )
            )
            logger.info("✓ Created index on behavior_logs.timestamp")

            # Index on behavior log employee_id for joins
            connection.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_behavior_log_employee 
                    ON behavior_logs(employee_id)
                    """
                )
            )
            logger.info("✓ Created index on behavior_logs.employee_id")

            # Index on alert creation for sorting
            connection.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_alert_created_at 
                    ON alerts(created_at DESC)
                    """
                )
            )
            logger.info("✓ Created index on alerts.created_at")

            connection.commit()

        logger.info("✓ Database initialization completed successfully")
        return True

    except Exception as exc:
        logger.error(f"✗ Database initialization failed: {exc}")
        return False


if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)
