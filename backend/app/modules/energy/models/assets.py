
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


class EnergyAsset(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_assets"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_asset_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "asset_code",
            name="uq_energy_asset_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_asset_facility_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "parent_asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_asset_parent_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_asset_tenant_facility",
            "tenant_id",
            "facility_id",
        ),
        Index(
            "ix_energy_asset_tenant_type_status",
            "tenant_id",
            "asset_type",
            "status",
        ),
        CheckConstraint(
            "rated_capacity_mw IS NULL OR rated_capacity_mw >= 0",
            name="ck_energy_asset_capacity_nonnegative",
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

    parent_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    asset_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    asset_category: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    model_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    serial_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    rated_capacity_mw: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
    )

    rated_voltage_kv: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
    )

    installation_date: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    commissioning_date: Mapped[str | None] = mapped_column(
        String(10),
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


class EnergyAssetComponent(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_asset_components"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_component_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "asset_id",
            "component_code",
            name="uq_energy_component_asset_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_component_asset_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_component_tenant_asset",
            "tenant_id",
            "asset_id",
        ),
        Index(
            "ix_energy_component_tenant_status",
            "tenant_id",
            "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    component_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    component_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    model_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    serial_reference: Mapped[str | None] = mapped_column(
        String(150),
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
