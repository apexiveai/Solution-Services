
import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.energy.models.common import (
    EnergyTenantMixin,
    EnergyTimestampMixin,
)


class EnergyOperatingUnit(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_operating_units"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_operating_unit_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "facility_id",
            "unit_code",
            name="uq_energy_operating_unit_facility_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_operating_unit_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_operating_unit_facility",
            "tenant_id",
            "facility_id",
        ),
        Index(
            "ix_energy_operating_unit_type_status",
            "tenant_id",
            "unit_type",
            "status",
        ),
        CheckConstraint(
            "rated_capacity_mw IS NULL OR rated_capacity_mw >= 0",
            name="ck_energy_operating_unit_capacity",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    facility_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    unit_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    unit_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    rated_capacity_mw: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
    )

    rated_voltage_kv: Mapped[Decimal | None] = mapped_column(
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
