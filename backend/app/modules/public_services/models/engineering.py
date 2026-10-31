import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.public_services.models.common import (
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
)


class PublicEngineeringProject(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_engineering_projects"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_project_tenant_id"),
        Index("ix_public_project_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contractor: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PLANNED")
    planned_progress: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=0
    )
    actual_progress: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=0
    )
    planned_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    planned_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    site_details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicEngineeringInspection(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_engineering_inspections"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "project_id"],
            ["public_engineering_projects.tenant_id", "public_engineering_projects.id"],
            name="fk_public_inspection_project_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_inspection_tenant_project", "tenant_id", "project_id"),
        Index("ix_public_inspection_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    inspection_type: Mapped[str] = mapped_column(String(64), nullable=False)
    inspector_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="OPEN")
    quality_findings: Mapped[str | None] = mapped_column(Text, nullable=True)
    safety_findings: Mapped[str | None] = mapped_column(Text, nullable=True)
    corrective_actions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicEngineeringProgressUpdate(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_engineering_progress_updates"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "project_id"],
            ["public_engineering_projects.tenant_id", "public_engineering_projects.id"],
            name="fk_public_progress_project_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_progress_tenant_project", "tenant_id", "project_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    progress_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    reported_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
