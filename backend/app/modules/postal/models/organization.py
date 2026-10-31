import uuid

from sqlalchemy import (
    String,
    Text,
    Boolean,
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


class PostalOrganization(Base, PostalTenantMixin, PostalTimestampMixin):
    __tablename__ = "postal_organizations"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_postal_org_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "organization_code",
            name="uq_postal_org_tenant_code",
        ),
        Index(
            "ix_postal_org_tenant_status",
            "tenant_id", "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_code: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    organization_type: Mapped[str] = mapped_column(
        String(40), default="POSTAL_OPERATOR", nullable=False
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


class PostalRegion(Base, PostalTenantMixin, PostalTimestampMixin):
    __tablename__ = "postal_regions"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_postal_region_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "region_code",
            name="uq_postal_region_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "organization_id"],
            ["postal_organizations.tenant_id", "postal_organizations.id"],
            ondelete="RESTRICT",
            name="fk_postal_region_organization_tenant",
        ),
        Index(
            "ix_postal_region_tenant_org",
            "tenant_id", "organization_id",
        ),
        Index(
            "ix_postal_region_tenant_status",
            "tenant_id", "status",
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


class PostalDistrict(Base, PostalTenantMixin, PostalTimestampMixin):
    __tablename__ = "postal_districts"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "id",
            name="uq_postal_district_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id", "region_id", "district_code",
            name="uq_postal_district_region_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "region_id"],
            ["postal_regions.tenant_id", "postal_regions.id"],
            ondelete="RESTRICT",
            name="fk_postal_district_region_tenant",
        ),
        Index(
            "ix_postal_district_tenant_region",
            "tenant_id", "region_id",
        ),
        Index(
            "ix_postal_district_tenant_status",
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