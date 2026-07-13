"""
Data Lifecycle Management — TTL and MongoDB Archival.

Handles:
- 30-minute auto-expiration of employee data
- MongoDB archival of important records before deletion
- Background cleanup tasks
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from uuid import UUID
import json
import logging

from sqlalchemy import and_
from sqlalchemy.orm import Session

from config import settings
from db import get_session
from models.database import Employee, BehaviorLog, CommunicationLog, Alert

logger = logging.getLogger(__name__)


class DataLifecycleService:
    """Manages data expiration and archival."""

    @staticmethod
    def set_expiration_on_employee(employee_id: UUID, ttl_minutes: int = 30) -> None:
        """
        Set an expiration timestamp on an employee record.
        After expiration, the record is eligible for deletion.

        Args:
            employee_id: Employee UUID
            ttl_minutes: Time-to-live in minutes (default: 30)
        """
        with get_session() as session:
            employee = session.query(Employee).filter(
                Employee.id == employee_id
            ).first()

            if not employee:
                logger.warning(f"Employee {employee_id} not found")
                return

            employee.expires_at = datetime.now(timezone.utc) + timedelta(
                minutes=ttl_minutes
            )
            session.commit()
            logger.info(
                f"Set expiration on employee {employee_id}: expires in {ttl_minutes} min"
            )

    @staticmethod
    def archive_employee_to_mongo(employee_id: UUID) -> bool:
        """
        Archive employee record and related logs to MongoDB before deletion.
        Preserves important audit trail and behavior data.

        Args:
            employee_id: Employee UUID

        Returns:
            True if archival succeeded, False otherwise
        """
        try:
            from db import get_mongo_database

            mongo_db = get_mongo_database()
            if not mongo_db:
                logger.warning("MongoDB not configured; skipping archival")
                return False

            with get_session() as session:
                employee = session.query(Employee).filter(
                    Employee.id == employee_id
                ).first()

                if not employee:
                    logger.warning(f"Employee {employee_id} not found for archival")
                    return False

                # Fetch related data
                behavior_logs = (
                    session.query(BehaviorLog)
                    .filter(BehaviorLog.employee_id == employee_id)
                    .all()
                )

                communication_logs = (
                    session.query(CommunicationLog)
                    .filter(CommunicationLog.employee_id == employee_id)
                    .all()
                )

                alerts = (
                    session.query(Alert)
                    .filter(Alert.employee_id == employee_id)
                    .all()
                )

                # Build archive document
                archive_doc = {
                    "archived_at": datetime.now(timezone.utc),
                    "employee": {
                        "id": str(employee.id),
                        "employee_code": employee.employee_code,
                        "full_name": employee.full_name,
                        "email": employee.email,
                        "role": employee.role.value,
                        "branch_id": str(employee.branch_id),
                        "is_active": employee.is_active,
                        "risk_score": employee.risk_score,
                        "created_at": employee.created_at.isoformat(),
                        "updated_at": employee.updated_at.isoformat(),
                    },
                    "behavior_logs": [
                        {
                            "id": str(log.id),
                            "event_type": log.event_type,
                            "event_detail": log.event_detail,
                            "ip_address": log.ip_address,
                            "anomaly_score": log.anomaly_score,
                            "timestamp": log.timestamp.isoformat(),
                        }
                        for log in behavior_logs
                    ],
                    "communication_logs": [
                        {
                            "id": str(log.id),
                            "communication_type": log.communication_type,
                            "content": log.content,
                            "recipient": log.recipient,
                            "created_at": log.created_at.isoformat(),
                        }
                        for log in communication_logs
                    ],
                    "alerts": [
                        {
                            "id": str(alert.id),
                            "alert_type": alert.alert_type,
                            "severity": alert.severity.value,
                            "status": alert.status.value,
                            "description": alert.description,
                            "created_at": alert.created_at.isoformat(),
                        }
                        for alert in alerts
                    ],
                }

                # Insert into MongoDB archive collection
                result = mongo_db["employee_archives"].insert_one(archive_doc)
                logger.info(
                    f"Archived employee {employee_id} to MongoDB: {result.inserted_id}"
                )
                return True

        except Exception as exc:
            logger.error(f"Failed to archive employee {employee_id}: {exc}")
            return False

    @staticmethod
    def delete_expired_employees() -> int:
        """
        Delete all employees whose expiration time has passed.
        Archives to MongoDB first.

        Returns:
            Number of employees deleted
        """
        now = datetime.now(timezone.utc)
        deleted_count = 0

        with get_session() as session:
            expired = session.query(Employee).filter(
                and_(
                    Employee.expires_at.isnot(None),
                    Employee.expires_at <= now,
                )
            ).all()

            for employee in expired:
                try:
                    # Archive before deletion
                    DataLifecycleService.archive_employee_to_mongo(employee.id)

                    # Delete employee (cascade will handle related records)
                    session.delete(employee)
                    deleted_count += 1

                except Exception as exc:
                    logger.error(
                        f"Failed to delete expired employee {employee.id}: {exc}"
                    )

            session.commit()
            logger.info(f"Deleted {deleted_count} expired employee records")

        return deleted_count

    @staticmethod
    def get_expiration_status(employee_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get expiration status for an employee.

        Returns:
            Dict with expiration time and remaining TTL, or None if not expiring
        """
        with get_session() as session:
            employee = session.query(Employee).filter(
                Employee.id == employee_id
            ).first()

            if not employee or not employee.expires_at:
                return None

            now = datetime.now(timezone.utc)
            remaining = employee.expires_at - now

            return {
                "expires_at": employee.expires_at.isoformat(),
                "remaining_seconds": remaining.total_seconds(),
                "is_expired": remaining.total_seconds() <= 0,
            }
