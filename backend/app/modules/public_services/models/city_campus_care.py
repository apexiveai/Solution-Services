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


class PublicCityAsset(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_city_assets"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_city_asset_tenant_id"),
        UniqueConstraint("tenant_id", "asset_code", name="uq_public_city_asset_tenant_code"),
        Index("ix_public_city_asset_tenant_type", "tenant_id", "asset_type"),
        Index("ix_public_city_asset_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(48), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    properties: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicCityTelemetry(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_city_telemetry"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            ["public_city_assets.tenant_id", "public_city_assets.id"],
            name="fk_public_city_telemetry_asset_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_city_telemetry_tenant_asset_time", "tenant_id", "asset_id", "observed_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_code: Mapped[str] = mapped_column(String(64), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(96), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublicCampus(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_campuses"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_campus_tenant_id"),
        Index("ix_public_campus_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    campus_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    campus_type: Mapped[str] = mapped_column(String(48), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    location: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    facilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicCampusAccessEvent(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_campus_access_events"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "campus_id"],
            ["public_campuses.tenant_id", "public_campuses.id"],
            name="fk_public_campus_access_campus_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_campus_access_tenant_time", "tenant_id", "occurred_at"),
        Index("ix_public_campus_access_tenant_campus", "tenant_id", "campus_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    campus_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    subject_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    access_point: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PublicCareRecipient(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_care_recipients"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_care_recipient_tenant_id"),
        Index("ix_public_care_recipient_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    care_level: Mapped[str] = mapped_column(String(32), nullable=False)
    contact_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    emergency_contact_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    care_preferences: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicCareVisit(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_care_visits"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "recipient_id"],
            ["public_care_recipients.tenant_id", "public_care_recipients.id"],
            name="fk_public_care_visit_recipient_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_care_visit_tenant_recipient", "tenant_id", "recipient_id"),
        Index("ix_public_care_visit_tenant_schedule", "tenant_id", "scheduled_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    caregiver_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="SCHEDULED")
    visit_notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class PublicCareAlert(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_care_alerts"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "recipient_id"],
            ["public_care_recipients.tenant_id", "public_care_recipients.id"],
            name="fk_public_care_alert_recipient_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_care_alert_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(48), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="OPEN")
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
