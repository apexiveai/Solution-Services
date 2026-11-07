import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Index, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.professional_services.common import (
    ProfessionalServicesRecordMixin,
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
)


class OperationProject(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_operation_projects"
    __table_args__ = (
        UniqueConstraint("tenant_id", "project_code", name="uq_ps_operation_project_code"),
        Index("ix_ps_operation_projects_tenant_status", "tenant_id", "status"),
    )

    project_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CustomerInsight(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_customer_insights"
    __table_args__ = (
        Index("ix_ps_customer_insights_tenant_customer", "tenant_id", "customer_reference"),
        Index("ix_ps_customer_insights_tenant_observed", "tenant_id", "observed_at"),
    )

    customer_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    insight_type: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class OperationCampaign(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_operation_campaigns"
    __table_args__ = (UniqueConstraint("tenant_id", "campaign_code", name="uq_ps_campaign_code"),)

    campaign_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    channel: Mapped[str] = mapped_column(String(48), nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    budget: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    audience: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class OperationTask(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_operation_tasks"
    __table_args__ = (Index("ix_ps_operation_tasks_tenant_due", "tenant_id", "due_at"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    campaign_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    task_type: Mapped[str] = mapped_column(String(64), nullable=False)
    assigned_to: Mapped[str | None] = mapped_column(String(128))
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OperationPerformance(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_operation_performance"
    __table_args__ = (
        Index("ix_ps_operation_performance_tenant_metric", "tenant_id", "metric_name"),
        Index("ix_ps_operation_performance_tenant_period", "tenant_id", "period_start"),
    )

    metric_name: Mapped[str] = mapped_column(String(96), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32))
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dimensions: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)