import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
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


class PublicEmergencyIncident(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_emergency_incidents"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_public_incident_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "incident_number",
            name="uq_public_incident_tenant_number",
        ),
        Index("ix_public_incident_tenant_status", "tenant_id", "status"),
        Index("ix_public_incident_tenant_type", "tenant_id", "incident_type"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    incident_number: Mapped[str] = mapped_column(String(64), nullable=False)
    incident_type: Mapped[str] = mapped_column(String(48), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="DISPATCH")
    severity: Mapped[str] = mapped_column(String(24), nullable=False, default="MEDIUM")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="REPORTED")
    reported_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    location: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class PublicResponseUnit(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_response_units"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_unit_tenant_id"),
        Index("ix_public_unit_tenant_status", "tenant_id", "status"),
        Index("ix_public_unit_tenant_type", "tenant_id", "unit_type"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    unit_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    unit_type: Mapped[str] = mapped_column(String(40), nullable=False)
    station_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="AVAILABLE")
    capabilities: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    current_location: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicDispatch(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_dispatches"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "incident_id"],
            ["public_emergency_incidents.tenant_id", "public_emergency_incidents.id"],
            name="fk_public_dispatch_incident_tenant",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "unit_id"],
            ["public_response_units.tenant_id", "public_response_units.id"],
            name="fk_public_dispatch_unit_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_public_dispatch_tenant_incident", "tenant_id", "incident_id"),
        Index("ix_public_dispatch_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    incident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="DISPATCHED")
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    arrived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class PublicEvidenceRecord(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_evidence_records"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "incident_id"],
            ["public_emergency_incidents.tenant_id", "public_emergency_incidents.id"],
            name="fk_public_evidence_incident_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_evidence_tenant_incident", "tenant_id", "incident_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    incident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(48), nullable=False)
    reference: Mapped[str] = mapped_column(String(500), nullable=False)
    collected_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    chain_of_custody: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
