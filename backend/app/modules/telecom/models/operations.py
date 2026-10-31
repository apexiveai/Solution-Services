
import uuid

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.telecom.models.common import (
    TelecomTenantMixin,
    TelecomTimestampMixin,
)


class TelecomAlarm(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_alarms"

    __table_args__ = (
        Index(
            "ix_telecom_alarms_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_telecom_alarms_tenant_severity",
            "tenant_id",
            "severity",
        ),
        Index(
            "ix_telecom_alarms_tenant_time",
            "tenant_id",
            "raised_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "telecom_monitoring_sources.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="SET NULL"),
        nullable=True,
    )

    interface_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_interfaces.id", ondelete="SET NULL"),
        nullable=True,
    )

    alarm_code: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    severity: Mapped[str] = mapped_column(
        String(24), default="WARNING", nullable=False
    )
    # CRITICAL, MAJOR, MINOR, WARNING, INFO

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )
    # ACTIVE, ACKNOWLEDGED, CLEARED

    raised_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    cleared_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    acknowledged_by: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    details: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )


class TelecomIncident(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_incidents"

    __table_args__ = (
        Index(
            "ix_telecom_incidents_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_telecom_incidents_tenant_priority",
            "tenant_id",
            "priority",
        ),
        Index(
            "ix_telecom_incidents_tenant_created",
            "tenant_id",
            "created_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    incident_number: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    alarm_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_alarms.id", ondelete="SET NULL"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(60), nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(24), default="P3", nullable=False
    )
    # P1, P2, P3, P4

    status: Mapped[str] = mapped_column(
        String(32), default="OPEN", nullable=False
    )
    # OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED

    assigned_to: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    resolution_notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    details: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
