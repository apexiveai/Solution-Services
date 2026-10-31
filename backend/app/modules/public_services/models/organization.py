import uuid

from sqlalchemy import (
    CheckConstraint,
    Index,
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


class PublicServiceOrganization(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_service_organizations"
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_public_org_tenant_code"),
        Index("ix_public_org_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    organization_type: Mapped[str] = mapped_column(String(48), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class PublicServiceLocation(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_service_locations"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_public_location_tenant_id"),
        UniqueConstraint("tenant_id", "code", name="uq_public_location_tenant_code"),
        Index("ix_public_location_tenant_type", "tenant_id", "location_type"),
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_public_location_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_public_location_longitude",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_type: Mapped[str] = mapped_column(String(48), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
