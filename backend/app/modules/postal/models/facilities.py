import uuid
from decimal import Decimal
from sqlalchemy import JSON
from sqlalchemy import (
    String,
    Text,
    Boolean,
    Numeric,
    CheckConstraint,
    Index,
    UniqueConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.postal.models.common import (
    PostalTenantMixin,
    PostalTimestampMixin,
)


class PostalFacility(Base, PostalTenantMixin, PostalTimestampMixin):
    __tablename__ = "postal_facilities"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_postal_facility_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "facility_code",
            name="uq_postal_facility_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "organization_id"],
            ["postal_organizations.tenant_id", "postal_organizations.id"],
            ondelete="RESTRICT",
            name="fk_postal_facility_organization_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "region_id"],
            ["postal_regions.tenant_id", "postal_regions.id"],
            ondelete="RESTRICT",
            name="fk_postal_facility_region_tenant",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "district_id"],
            ["postal_districts.tenant_id", "postal_districts.id"],
            ondelete="RESTRICT",
            name="fk_postal_facility_district_tenant",
        ),
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_postal_facility_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_postal_facility_longitude",
        ),
        Index(
            "ix_postal_facility_tenant_type",
            "tenant_id", "facility_type",
        ),
        Index(
            "ix_postal_facility_tenant_status",
            "tenant_id", "status",
        ),
        Index(
            "ix_postal_facility_tenant_region",
            "tenant_id", "region_id",
        ),
        Index(
            "ix_postal_facility_tenant_district",
            "tenant_id", "district_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    region_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    district_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    parent_facility_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    facility_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    facility_type: Mapped[str] = mapped_column(
        String(40), nullable=False
    )

    facility_level: Mapped[str] = mapped_column(
        String(40), default="STANDARD", nullable=False
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )

    country_code: Mapped[str] = mapped_column(
        String(2), default="MM", nullable=False
    )

    city: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        Text, nullable=True
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

    operating_hours: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
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