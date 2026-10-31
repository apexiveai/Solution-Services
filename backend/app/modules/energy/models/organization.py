
import uuid

from sqlalchemy import (
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.energy.models.common import (
    EnergyTenantMixin,
    EnergyTimestampMixin,
)


class EnergyFacility(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_facilities"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_facility_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "facility_code",
            name="uq_energy_facility_tenant_code",
        ),
        Index(
            "ix_energy_facility_tenant_type",
            "tenant_id",
            "facility_type",
        ),
        Index(
            "ix_energy_facility_tenant_status",
            "tenant_id",
            "status",
        ),
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_energy_facility_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_energy_facility_longitude",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    facility_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    facility_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    generation_type: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    voltage_level: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
    )

    installed_capacity_mw: Mapped[float | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
    )

    operational_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="UNKNOWN",
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ACTIVE",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
