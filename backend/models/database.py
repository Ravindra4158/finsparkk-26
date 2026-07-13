"""
BankGuard Enterprise — SQLAlchemy ORM Models.

Defines the relational schema for the core banking surveillance platform.
All tables use UUID primary keys and carry automatic ``created_at`` /
``updated_at`` audit columns via the ``AuditMixin``.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ── Base & Mixins ────────────────────────────────────────────────────────


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    pass


class AuditMixin:
    """Adds ``created_at`` and ``updated_at`` columns to every model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


# ── Enumerations ─────────────────────────────────────────────────────────


class AlertSeverity(str, enum.Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    """Lifecycle status of an alert."""
    OPEN = "open"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class LoanStatus(str, enum.Enum):
    """Loan application status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    FLAGGED = "flagged"


class SwiftMessageStatus(str, enum.Enum):
    """SWIFT message reconciliation status."""
    PENDING = "pending"
    MATCHED = "matched"
    UNMATCHED = "unmatched"
    RECONCILED = "reconciled"


class EmployeeRole(str, enum.Enum):
    """Internal roles for employees."""
    TELLER = "teller"
    LOAN_OFFICER = "loan_officer"
    BRANCH_MANAGER = "branch_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    ADMIN = "admin"


# ── Models ───────────────────────────────────────────────────────────────


class Branch(AuditMixin, Base):
    """Bank branch location."""

    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    employees: Mapped[List["Employee"]] = relationship(back_populates="branch")
    loans: Mapped[List["Loan"]] = relationship(back_populates="branch")


class Employee(AuditMixin, Base):
    """Bank employee / user account."""

    __tablename__ = "employees"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_code: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[EmployeeRole] = mapped_column(
        Enum(EmployeeRole), default=EmployeeRole.TELLER
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    risk_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        comment="Employee data auto-expires and is deleted after 30 minutes"
    )

    # Relationships
    branch: Mapped["Branch"] = relationship(back_populates="employees")
    behavior_logs: Mapped[List["BehaviorLog"]] = relationship(
        back_populates="employee"
    )
    communication_logs: Mapped[List["CommunicationLog"]] = relationship(
        back_populates="employee"
    )
    alerts: Mapped[List["Alert"]] = relationship(back_populates="employee")


class BehaviorLog(AuditMixin, Base):
    """Time-series log of employee behaviour signals (login, transactions, etc.)."""

    __tablename__ = "behavior_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    device_fingerprint: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    anomaly_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="behavior_logs")


class Applicant(AuditMixin, Base):
    """External loan applicant."""

    __tablename__ = "applicants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    pan_number: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    aadhaar_hash: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    annual_income: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    credit_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    loans: Mapped[List["Loan"]] = relationship(back_populates="applicant")


class Loan(AuditMixin, Base):
    """Loan application record."""

    __tablename__ = "loans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    loan_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    applicant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("applicants.id"), nullable=False
    )
    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    interest_rate: Mapped[float] = mapped_column(Float, nullable=False)
    purpose: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus), default=LoanStatus.PENDING
    )
    risk_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    risk_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    applicant: Mapped["Applicant"] = relationship(back_populates="loans")
    branch: Mapped["Branch"] = relationship(back_populates="loans")
    compliance_checkpoints: Mapped[List["ComplianceCheckpoint"]] = relationship(
        back_populates="loan"
    )


class ComplianceCheckpoint(AuditMixin, Base):
    """Audit trail for compliance checks on a loan."""

    __tablename__ = "compliance_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loans.id"), nullable=False
    )
    checkpoint_name: Mapped[str] = mapped_column(String(200), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True
    )

    # Relationships
    loan: Mapped["Loan"] = relationship(back_populates="compliance_checkpoints")


class SwiftMessage(AuditMixin, Base):
    """Inbound/outbound SWIFT message for reconciliation."""

    __tablename__ = "swift_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    message_type: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # e.g. MT103, MT202
    sender_bic: Mapped[str] = mapped_column(String(11), nullable=False)
    receiver_bic: Mapped[str] = mapped_column(String(11), nullable=False)
    reference: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    value_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    raw_payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[SwiftMessageStatus] = mapped_column(
        Enum(SwiftMessageStatus), default=SwiftMessageStatus.PENDING
    )

    # Relationships
    cbs_records: Mapped[List["CbsRecord"]] = relationship(
        back_populates="swift_message"
    )


class CbsRecord(AuditMixin, Base):
    """Core Banking System transaction record used for SWIFT reconciliation."""

    __tablename__ = "cbs_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transaction_ref: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    booking_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    swift_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("swift_messages.id"),
        nullable=True,
    )

    # Relationships
    swift_message: Mapped[Optional["SwiftMessage"]] = relationship(
        back_populates="cbs_records"
    )


class CommunicationLog(AuditMixin, Base):
    """Captured employee communication metadata (email subjects, chat flags)."""

    __tablename__ = "communication_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False
    )
    channel: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # email, chat, phone
    subject: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    employee: Mapped["Employee"] = relationship(
        back_populates="communication_logs"
    )


class Alert(AuditMixin, Base):
    """Risk alert generated by the platform."""

    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity), default=AlertSeverity.MEDIUM
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus), default=AlertStatus.OPEN
    )
    category: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # ueba, loan_fraud, swift, compliance
    employee_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True
    )
    loan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loans.id"), nullable=True
    )
    risk_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    employee: Mapped[Optional["Employee"]] = relationship(
        back_populates="alerts"
    )
