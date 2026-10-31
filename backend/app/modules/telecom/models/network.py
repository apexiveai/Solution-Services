
import uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.telecom.models.common import (
    TelecomTenantMixin,
    TelecomTimestampMixin,
)


class TelecomModule(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_modules"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "module_code",
            name="uq_telecom_module_tenant_code",
        ),
        Index("ix_telecom_modules_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    module_code: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(24), default="ACTIVE")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class TelecomSite(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_sites"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "site_code",
            name="uq_telecom_site_tenant_code",
        ),
        Index("ix_telecom_sites_tenant_type", "tenant_id", "site_type"),
        Index("ix_telecom_sites_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    site_code: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    site_type: Mapped[str] = mapped_column(
        String(40), nullable=False
    )  # TOWER, DATA_CENTER, POP

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(3), nullable=True)

    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)

    elevation_meters: Mapped[float | None] = mapped_column(nullable=True)

    metadata_json: Mapped[dict] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )


class TelecomDevice(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_devices"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "device_code",
            name="uq_telecom_device_tenant_code",
        ),
        Index("ix_telecom_devices_tenant_type", "tenant_id", "device_type"),
        Index("ix_telecom_devices_tenant_status", "tenant_id", "status"),
        Index("ix_telecom_devices_site", "tenant_id", "site_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_sites.id", ondelete="SET NULL"),
        nullable=True,
    )

    device_code: Mapped[str] = mapped_column(String(100), nullable=False)
    hostname: Mapped[str] = mapped_column(String(200), nullable=False)

    device_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # ROUTER, OLT, BTS, SWITCH

    vendor: Mapped[str | None] = mapped_column(String(120), nullable=True)
    model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(String(150), nullable=True)

    management_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    management_port: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(
        String(24), default="UNKNOWN", nullable=False
    )

    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    metadata_json: Mapped[dict] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )


class TelecomInterface(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_interfaces"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "device_id", "interface_name",
            name="uq_telecom_interface_device_name",
        ),
        Index("ix_telecom_interfaces_device", "tenant_id", "device_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    interface_name: Mapped[str] = mapped_column(String(120), nullable=False)
    interface_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    mac_address: Mapped[str | None] = mapped_column(String(32), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    speed_mbps: Mapped[int | None] = mapped_column(Integer, nullable=True)

    admin_status: Mapped[str] = mapped_column(
        String(24), default="UNKNOWN", nullable=False
    )
    operational_status: Mapped[str] = mapped_column(
        String(24), default="UNKNOWN", nullable=False
    )

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class TelecomConnection(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_connections"

    __table_args__ = (
        Index("ix_telecom_connections_source", "tenant_id", "source_device_id"),
        Index("ix_telecom_connections_target", "tenant_id", "target_device_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    target_device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    source_interface_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_interfaces.id", ondelete="SET NULL"),
        nullable=True,
    )

    target_interface_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_interfaces.id", ondelete="SET NULL"),
        nullable=True,
    )

    connection_type: Mapped[str] = mapped_column(
        String(40), default="PHYSICAL", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="UNKNOWN", nullable=False
    )

    bandwidth_mbps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class TelecomTopologyLink(Base, TelecomTenantMixin, TelecomTimestampMixin):
    __tablename__ = "telecom_topology_links"

    __table_args__ = (
        Index("ix_telecom_topology_source", "tenant_id", "source_device_id"),
        Index("ix_telecom_topology_target", "tenant_id", "target_device_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    target_device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_devices.id", ondelete="CASCADE"),
        nullable=False,
    )

    connection_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telecom_connections.id", ondelete="SET NULL"),
        nullable=True,
    )

    link_type: Mapped[str] = mapped_column(
        String(40), default="NETWORK", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="UNKNOWN", nullable=False
    )

    label: Mapped[str | None] = mapped_column(String(200), nullable=True)

    metadata_json: Mapped[dict] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )
