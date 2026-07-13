"""
Background Task Scheduler for Data Lifecycle Management.

Runs periodic cleanup tasks using APScheduler:
- Every 5 minutes: Delete expired employees and archive to MongoDB
- Runs in a background thread alongside FastAPI
"""

import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from services.data_lifecycle import DataLifecycleService

logger = logging.getLogger(__name__)


class DataCleanupScheduler:
    """Manages background cleanup tasks."""

    _scheduler: BackgroundScheduler = None

    @classmethod
    def start(cls):
        """Start the background scheduler."""
        if cls._scheduler is not None:
            logger.warning("Scheduler already running")
            return

        cls._scheduler = BackgroundScheduler()

        # Schedule employee expiration cleanup every 5 minutes
        cls._scheduler.add_job(
            cls._cleanup_expired_employees,
            trigger=IntervalTrigger(minutes=5),
            id="cleanup_expired_employees",
            name="Cleanup expired employee records and archive to MongoDB",
            replace_existing=True,
        )

        cls._scheduler.start()
        logger.info("✓ Data cleanup scheduler started")

    @classmethod
    def stop(cls):
        """Stop the background scheduler."""
        if cls._scheduler is None:
            logger.warning("Scheduler not running")
            return

        cls._scheduler.shutdown()
        cls._scheduler = None
        logger.info("✓ Data cleanup scheduler stopped")

    @classmethod
    def _cleanup_expired_employees(cls):
        """Background task: Delete expired employees."""
        try:
            now = datetime.now(timezone.utc).isoformat()
            deleted = DataLifecycleService.delete_expired_employees()
            if deleted > 0:
                logger.info(f"[{now}] Cleaned up {deleted} expired employees")
        except Exception as exc:
            logger.error(f"Cleanup task failed: {exc}")
