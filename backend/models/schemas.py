"""
BankGuard Enterprise — Pydantic Schemas.

Defines Pydantic models for request/response validation in FastAPI.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from .database import AlertSeverity, AlertStatus, LoanStatus, SwiftMessageStatus, EmployeeRole


# ── Common ───────────────────────────────────────────────────────────────

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Employee ──────────────────────────────────────────────────────────────

class EmployeeBase(BaseSchema):
    employee_code: str
    full_name: str
    email: EmailStr
    role: EmployeeRole
    branch_id: UUID
    is_active: bool = True
    risk_score: Optional[float] = None

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeResponse(EmployeeBase):
    id: UUID
    created_at: datetime
    expires_at: Optional[datetime] = None


# ── Applicant ─────────────────────────────────────────────────────────────

class ApplicantBase(BaseSchema):
    full_name: str
    pan_number: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    annual_income: Optional[float] = None
    credit_score: Optional[int] = None

class ApplicantCreate(ApplicantBase):
    pass

class ApplicantResponse(ApplicantBase):
    id: UUID
    created_at: datetime


# ── Loan ──────────────────────────────────────────────────────────────────

class LoanBase(BaseSchema):
    loan_number: str
    applicant_id: UUID
    branch_id: UUID
    amount: float
    tenure_months: int
    interest_rate: float
    purpose: Optional[str] = None
    status: LoanStatus = LoanStatus.PENDING

class LoanCreate(LoanBase):
    pass

class LoanResponse(LoanBase):
    id: UUID
    risk_score: Optional[float] = None
    risk_explanation: Optional[str] = None
    created_at: datetime


# ── SWIFT Message ─────────────────────────────────────────────────────────

class SwiftMessageBase(BaseSchema):
    message_type: str
    sender_bic: str
    receiver_bic: str
    reference: str
    amount: float
    currency: str
    value_date: datetime
    status: SwiftMessageStatus = SwiftMessageStatus.PENDING

class SwiftMessageCreate(SwiftMessageBase):
    raw_payload: Optional[str] = None

class SwiftMessageResponse(SwiftMessageBase):
    id: UUID
    created_at: datetime


# ── Alert ─────────────────────────────────────────────────────────────────

class AlertBase(BaseSchema):
    title: str
    description: Optional[str] = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    status: AlertStatus = AlertStatus.OPEN
    category: str
    employee_id: Optional[UUID] = None
    loan_id: Optional[UUID] = None
    risk_score: Optional[float] = None

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: UUID
    explanation: Optional[str] = None
    created_at: datetime

# ── Authentication ───────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
