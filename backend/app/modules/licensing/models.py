import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CoreRpaOpportunity(Base):
    __tablename__ = "core_rpa_opportunities"
    __table_args__ = (
        CheckConstraint(
            "request_kind IN ('SERVICE', 'LICENSE', 'RENEWAL')",
            name="ck_core_rpa_opportunity_kind",
        ),
        CheckConstraint(
            "status IN ('SUBMITTED', 'ASSESSMENT', 'POC', 'QUOTED', 'ACCEPTED', 'DECLINED', 'COMPLETED')",
            name="ck_core_rpa_opportunity_status",
        ),
        Index("ix_core_rpa_opportunity_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    request_kind: Mapped[str] = mapped_column(String(20), nullable=False)
    service_type: Mapped[str] = mapped_column(String(80), nullable=False)
    departments: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    requested_developers: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    requested_bots: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    plan_code: Mapped[str] = mapped_column(String(60), nullable=False, default="ENTERPRISE")
    approved_developers: Mapped[int | None] = mapped_column(Integer, nullable=True)
    approved_bots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    approved_monthly_executions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    deployment: Mapped[str] = mapped_column(String(24), nullable=False, default="AEOP_CLOUD")
    requirements: Mapped[str] = mapped_column(Text, nullable=False, default="")
    renewal_license_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("core_rpa_licenses.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="SUBMITTED")
    quote_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MMK")
    quote_valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    quote_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class CoreRpaOrder(Base):
    __tablename__ = "core_rpa_orders"
    __table_args__ = (
        CheckConstraint(
            "status IN ('AGREEMENT_REQUIRED', 'PAYMENT_DUE', 'PAYMENT_REVIEW', 'ACTIVE', 'CANCELLED')",
            name="ck_core_rpa_order_status",
        ),
        Index("ix_core_rpa_order_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("core_rpa_opportunities.id", ondelete="RESTRICT"), nullable=False
    )
    order_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    plan_code: Mapped[str] = mapped_column(String(60), nullable=False)
    developer_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    bot_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_execution_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    deployment: Mapped[str] = mapped_column(String(24), nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    renewal_license_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("core_rpa_licenses.id", ondelete="SET NULL"), nullable=True
    )
    agreement_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    agreement_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agreement_accepted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agreement_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="AGREEMENT_REQUIRED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class CoreRpaLicense(Base):
    __tablename__ = "core_rpa_licenses"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'EXPIRED')",
            name="ck_core_rpa_license_status",
        ),
        Index("ix_core_rpa_license_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("core_rpa_orders.id", ondelete="RESTRICT"), nullable=False
    )
    plan_code: Mapped[str] = mapped_column(String(60), nullable=False)
    developer_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    bot_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_execution_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    deployment: Mapped[str] = mapped_column(String(24), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)


class CoreRpaDeveloperSeat(Base):
    __tablename__ = "core_rpa_developer_seats"
    __table_args__ = (
        Index("ix_core_rpa_developer_seat_tenant", "tenant_id"),
        UniqueConstraint("tenant_id", "subject", name="uq_core_rpa_developer_seat_subject"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
