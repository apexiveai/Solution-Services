import uuid
from decimal import Decimal

from sqlalchemy import (
    String,
    Text,
    Numeric,
    Boolean,
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


class HighwayNetwork(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_highway_networks"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_highway_network_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "network_code",
            name="uq_transport_highway_network_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "operator_id"],
            [
                "transportation_operators.tenant_id",
                "transportation_operators.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_highway_operator_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "region_id"],
            [
                "transportation_regions.tenant_id",
                "transportation_regions.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_highway_region_tenant",
        ),
        CheckConstraint(
            "total_length_km IS NULL OR total_length_km >= 0",
            name="ck_transport_highway_length",
        ),
        Index(
            "ix_transport_highway_tenant_operator",
            "tenant_id", "operator_id",
        ),
        Index(
            "ix_transport_highway_tenant_region",
            "tenant_id", "region_id",
        ),
        Index(
            "ix_transport_highway_tenant_status",
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

    network_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    network_type: Mapped[str] = mapped_column(
        String(40), default="EXPRESSWAY", nullable=False
    )

    road_classification: Mapped[str] = mapped_column(
        String(40), default="PRIMARY", nullable=False
    )

    start_location: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )

    end_location: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )

    total_length_km: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4), nullable=True
    )

    number_of_sections: Mapped[int] = mapped_column(
        default=0, nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )


class RoadSection(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_road_sections"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_road_section_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "network_id", "section_code",
            name="uq_transport_road_section_network_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "network_id"],
            [
                "transportation_highway_networks.tenant_id",
                "transportation_highway_networks.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_road_section_network_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "district_id"],
            [
                "transportation_districts.tenant_id",
                "transportation_districts.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_road_section_district_tenant",
        ),
        CheckConstraint(
            "length_km IS NULL OR length_km >= 0",
            name="ck_transport_road_section_length",
        ),
        CheckConstraint(
            "speed_limit_kph IS NULL OR speed_limit_kph > 0",
            name="ck_transport_road_section_speed",
        ),
        Index(
            "ix_transport_road_section_tenant_network",
            "tenant_id", "network_id",
        ),
        Index(
            "ix_transport_road_section_tenant_district",
            "tenant_id", "district_id",
        ),
        Index(
            "ix_transport_road_section_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    network_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    district_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    section_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    start_km: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4), nullable=True
    )

    end_km: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4), nullable=True
    )

    length_km: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4), nullable=True
    )

    speed_limit_kph: Mapped[int | None] = mapped_column(
        nullable=True
    )

    carriageway_type: Mapped[str] = mapped_column(
        String(32), default="DUAL", nullable=False
    )

    lane_count: Mapped[int] = mapped_column(
        default=2, nullable=False
    )

    surface_type: Mapped[str | None] = mapped_column(
        String(40), nullable=True
    )

    operational_status: Mapped[str] = mapped_column(
        String(32), default="UNKNOWN", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )


class RoadLane(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_road_lanes"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_road_lane_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "section_id", "lane_code",
            name="uq_transport_road_lane_section_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "section_id"],
            [
                "transportation_road_sections.tenant_id",
                "transportation_road_sections.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_road_lane_section_tenant",
        ),
        Index(
            "ix_transport_road_lane_tenant_section",
            "tenant_id", "section_id",
        ),
        Index(
            "ix_transport_road_lane_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    lane_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    lane_number: Mapped[int] = mapped_column(
        nullable=False
    )

    direction: Mapped[str] = mapped_column(
        String(24), default="FORWARD", nullable=False
    )

    lane_type: Mapped[str] = mapped_column(
        String(40), default="GENERAL", nullable=False
    )

    is_toll_lane: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    operational_status: Mapped[str] = mapped_column(
        String(32), default="UNKNOWN", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )