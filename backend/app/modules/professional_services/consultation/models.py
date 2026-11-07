import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, JSON, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.professional_services.common import (
    ProfessionalServicesRecordMixin,
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
)


class ConsultationProject(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_consultation_projects"
    __table_args__ = (
        UniqueConstraint("tenant_id", "project_code", name="uq_ps_consult_project_code"),
        Index("ix_ps_consult_projects_tenant_status", "tenant_id", "status"),
    )

    project_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    project_type: Mapped[str] = mapped_column(String(64), nullable=False)
    client_reference: Mapped[str | None] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(Text)


class ConsultationAssessment(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_consultation_assessments"
    __table_args__ = (Index("ix_ps_assessments_tenant_project", "tenant_id", "project_id"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(64), nullable=False)
    assessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    findings: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class ConsultationStrategy(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_consultation_strategies"
    __table_args__ = (Index("ix_ps_strategies_tenant_project", "tenant_id", "project_id"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    strategy_type: Mapped[str] = mapped_column(String(64), nullable=False)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    objectives: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)


class ConsultationRoadmap(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_consultation_roadmaps"
    __table_args__ = (Index("ix_ps_roadmaps_tenant_project", "tenant_id", "project_id"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    target_completion_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    milestones: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)


class ConsultationDeliverable(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_consultation_deliverables"
    __table_args__ = (Index("ix_ps_deliverables_tenant_project", "tenant_id", "project_id"),)

    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    deliverable_type: Mapped[str] = mapped_column(String(64), nullable=False)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))