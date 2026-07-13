from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4
from datetime import datetime

from models.schemas import SwiftMessageResponse, SwiftMessageCreate
from models.database import SwiftMessageStatus
from utils.security import require_role

MANAGER_ROLES = ["admin", "branch_manager", "compliance_officer"]

router = APIRouter(dependencies=[Depends(require_role(MANAGER_ROLES))])

@router.get("/", response_model=List[SwiftMessageResponse])
async def list_swift_messages():
    """List SWIFT messages for compliance auditing."""
    return [
        {
            "id": uuid4(),
            "message_type": "MT799",
            "sender_bic": "PNBXXXXX",
            "receiver_bic": "HSBCXXXX",
            "reference": "REF-12345",
            "amount": 4000000,
            "currency": "USD",
            "value_date": datetime.utcnow(),
            "status": SwiftMessageStatus.UNMATCHED,
            "created_at": datetime.utcnow()
        }
    ]

@router.post("/", response_model=SwiftMessageResponse)
async def ingest_swift(msg: SwiftMessageCreate):
    """Ingest a SWIFT message and cross-check with CBS."""
    new_msg = msg.dict()
    new_msg["id"] = uuid4()
    new_msg["status"] = SwiftMessageStatus.UNMATCHED  # Simulated rules engine output
    new_msg["created_at"] = datetime.utcnow()
    return new_msg
