from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4
from datetime import datetime

from models.schemas import AlertResponse
from models.database import AlertSeverity, AlertStatus
from utils.security import require_role

MANAGER_ROLES = ["admin", "branch_manager", "compliance_officer"]

router = APIRouter(dependencies=[Depends(require_role(MANAGER_ROLES))])

MOCK_ALERTS = [
    {
        "id": uuid4(),
        "title": "Abnormal SWIFT MT799 Issued",
        "description": "LoU issued without matching CBS record.",
        "severity": AlertSeverity.CRITICAL,
        "status": AlertStatus.OPEN,
        "category": "swift_cbs",
        "risk_score": 98.5,
        "explanation": "No CBS record found for $4M SWIFT transaction.",
        "created_at": datetime.utcnow()
    },
    {
        "id": uuid4(),
        "title": "Off-hours Login Detected",
        "description": "Manager logged in at 2:30 AM from unusual IP.",
        "severity": AlertSeverity.HIGH,
        "status": AlertStatus.OPEN,
        "category": "ueba",
        "risk_score": 85.0,
        "explanation": "Login time is 14.2σ from peer baseline.",
        "created_at": datetime.utcnow()
    }
]

@router.get("/", response_model=List[AlertResponse])
async def list_alerts():
    """Get list of active alerts."""
    return MOCK_ALERTS

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str):
    """Get specific alert details."""
    return MOCK_ALERTS[0]
