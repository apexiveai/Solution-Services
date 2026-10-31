import uuid
from decimal import Decimal

from sqlalchemy import (
    String,
    Text,
    Numeric,
    CheckConstraint,
    Index,
    UniqueConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.transportation.models.common import (
    TransportationTenantMixin,
    TransportationTimestampMixin,
)


class TransportationFacility(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_facilities"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_facility_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "facility_code",
            name="uq_transport_facility_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "operator_id"],
            [
                "transportation_operators.tenant_id",
                "transportation_operators.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_facility_operator_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "region_id"],
            [
                "transportation_regions.tenant_id",
                "transportation_regions.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_facility_region_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "district_id"],
            [
                "transportation_districts.tenant_id",
                "transportation_districts.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_facility_district_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "network_id"],
            [
                "transportation_highway_networks.tenant_id",
                "transportation_highway_networks.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_facility_network_tenant",
        ),
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_transport_facility_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_transport_facility_longitude",
        ),
        Index(
            "ix_transport_facility_tenant_operator",
            "tenant_id", "operator_id",
        ),
        Index(
            "ix_transport_facility_tenant_type",
            "tenant_id", "facility_type",
        ),
        Index(
            "ix_transport_facility_tenant_region",
            "tenant_id", "region_id",
        ),
        Index(
            "ix_transport_facility_tenant_network",
            "tenant_id", "network_id",
        ),
        Index(
            "ix_transport_facility_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    region_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    district_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    network_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    facility_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    facility_type: Mapped[str] = mapped_column(
        String(48), nullable=False
    )

    facility_level: Mapped[str] = mapped_column(
        String(40), default="STANDARD", nullable=False
    )

    address: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    city: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )

    timezone: Mapped[str] = mapped_column(
        String(64), default="Asia/Yangon", nullable=False
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(40), nullable=True
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(254), nullable=True
    )

    operating_status: Mapped[str] = mapped_column(
        String(32), default="UNKNOWN", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )