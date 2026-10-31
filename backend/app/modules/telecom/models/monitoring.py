
import uuid

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
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


class TelecomMonitoringSource(
    Base, TelecomTenantMixin, TelecomTimestampMixin
):
    __tablename__ = "telecom_monitoring_sources"

    __table_args__ = (
        Index(
            "ix_telecom_monitoring_tenant_type",
            "tenant_id",
            "source_type",
        ),
        Index(
            "ix_telecom_monitoring_tenant_status",
            "tenant_id",
            "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=True,
    )

    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_sites.id", ondelete="CASCADE"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String(160), nullable=False)

    source_type: Mapped[str] = mapped_column(
        String(40), nullable=False
    )
    # SNMP, SNMP_TRAP, SYSLOG, REST_API,
    # NETCONF, RESTCONF, STREAMING_TELEMETRY

    endpoint: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    port: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(
        String(24), default="INACTIVE", nullable=False
    )

    polling_interval_seconds: Mapped[int] = mapped_column(
        Integer, default=60, nullable=False
    )

    configuration: Mapped[dict] = mapped_column(
        "configuration", JSON, default=dict, nullable=False
    )

    # Store secret references, not raw passwords/community strings.
    credential_reference: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    last_error: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )


class TelecomMetricSample(Base, TelecomTenantMixin):
    __tablename__ = "telecom_metric_samples"

    __table_args__ = (
        Index(
            "ix_telecom_metrics_tenant_time",
            "tenant_id",
            "collected_at",
        ),
        Index(
            "ix_telecom_metrics_device_time",
            "tenant_id",
            "device_id",
            "collected_at",
        ),
        Index(
            "ix_telecom_metrics_name_time",
            "tenant_id",
            "metric_name",
            "collected_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "telecom_monitoring_sources.id",
            ondelete="CASCADE",
        ),
        nullable=False,
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

    metric_name: Mapped[str] = mapped_column(
        String(120), nullable=False
    )

    metric_category: Mapped[str] = mapped_column(
        String(60), nullable=False
    )
    # CPU, MEMORY, BANDWIDTH, LATENCY, PACKET_LOSS, etc.

    metric_value: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(32), default="value", nullable=False
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    labels: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
