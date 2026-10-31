import uuid

from sqlalchemy import (
    String,
    Text,
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


class TransportationOperator(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_operators"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_operator_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "operator_code",
            name="uq_transport_operator_code",
        ),
        Index(
            "ix_transport_operator_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    operator_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    operator_type: Mapped[str] = mapped_column(
        String(48), default="HIGHWAY_OPERATOR", nullable=False
    )

    country_code: Mapped[str] = mapped_column(
        String(2), default="MM", nullable=False
    )

    registration_reference: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(254), nullable=True
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(40), nullable=True
    )

    website: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )


class TransportationRegion(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_regions"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_region_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "region_code",
            name="uq_transport_region_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "operator_id"],
            [
                "transportation_operators.tenant_id",
                "transportation_operators.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_region_operator_tenant",
        ),
        Index(
            "ix_transport_region_tenant_operator",
            "tenant_id", "operator_id",
        ),
        Index(
            "ix_transport_region_tenant_status",
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

    region_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(160), nullable=False
    )

    region_type: Mapped[str] = mapped_column(
        String(40), default="ADMINISTRATIVE_REGION", nullable=False
    )

    country_code: Mapped[str] = mapped_column(
        String(2), default="MM", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )


class TransportationDistrict(
    Base,
    TransportationTenantMixin,
    TransportationTimestampMixin,
):
    __tablename__ = "transportation_districts"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_transport_district_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "region_id", "district_code",
            name="uq_transport_district_region_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "region_id"],
            [
                "transportation_regions.tenant_id",
                "transportation_regions.id",
            ],
            ondelete="RESTRICT",
            name="fk_transport_district_region_tenant",
        ),
        Index(
            "ix_transport_district_tenant_region",
            "tenant_id", "region_id",
        ),
        Index(
            "ix_transport_district_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    region_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    district_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(160), nullable=False
    )

    district_type: Mapped[str] = mapped_column(
        String(40), default="DISTRICT", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(24), default="ACTIVE", nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )