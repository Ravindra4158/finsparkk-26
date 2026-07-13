from fastapi import APIRouter, Depends
from typing import List
from uuid import uuid4
from datetime import datetime

from models.schemas import LoanResponse, LoanCreate
from models.database import LoanStatus
from utils.security import require_role

BRANCH_ROLES = ["admin", "branch_manager", "loan_officer", "teller"]

router = APIRouter(dependencies=[Depends(require_role(BRANCH_ROLES))])

MOCK_LOANS = [
    {
        "id": uuid4(),
        "loan_number": "LN-8842",
        "applicant_id": uuid4(),
        "branch_id": uuid4(),
        "amount": 2500000,
        "tenure_months": 240,
        "interest_rate": 8.5,
        "purpose": "Commercial Real Estate",
        "status": LoanStatus.FLAGGED,
        "risk_score": 88.0,
        "risk_explanation": "Applicant has hidden graph links to manager's brother.",
        "created_at": datetime.utcnow()
    }
]

@router.get("/", response_model=List[LoanResponse])
async def list_loans():
    """List loan applications and their risk scores."""
    return MOCK_LOANS

@router.post("/", response_model=LoanResponse)
async def apply_loan(loan: LoanCreate):
    """Submit a loan application. Triggers ML risk analysis."""
    new_loan = loan.dict()
    new_loan["id"] = uuid4()
    new_loan["risk_score"] = 45.0  # Simulated ML score
    new_loan["risk_explanation"] = "Standard profile, no immediate anomalies."
    new_loan["created_at"] = datetime.utcnow()
    return new_loan
