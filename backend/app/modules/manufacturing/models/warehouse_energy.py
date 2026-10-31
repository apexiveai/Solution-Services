import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.manufacturing.models.common import (
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
)


class ManufacturingWarehouse(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_warehouses"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_mfg_warehouse_tenant_id"),
        UniqueConstraint("tenant_id", "warehouse_code", name="uq_mfg_warehouse_tenant_code"),
        ForeignKeyConstraint(
            ["tenant_id", "facility_code"],
            ["manufacturing_facilities.tenant_id", "manufacturing_facilities.facility_code"],
            name="fk_mfg_warehouse_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_warehouse_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    warehouse_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    facility_code: Mapped[str] = mapped_column(String(64), nullable=False)
    warehouse_type: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")


class ManufacturingInventoryBalance(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_inventory_balances"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "warehouse_code",
            "item_code",
            name="uq_mfg_inventory_tenant_warehouse_item",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "warehouse_code"],
            ["manufacturing_warehouses.tenant_id", "manufacturing_warehouses.warehouse_code"],
            name="fk_mfg_inventory_warehouse_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_mfg_inventory_tenant_item", "tenant_id", "item_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    warehouse_code: Mapped[str] = mapped_column(String(64), nullable=False)
    item_code: Mapped[str] = mapped_column(String(64), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    item_type: Mapped[str] = mapped_column(String(40), nullable=False)
    quantity_on_hand: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), nullable=False, default=0
    )
    quantity_reserved: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), nullable=False, default=0
    )
    unit_of_measure: Mapped[str] = mapped_column(String(24), nullable=False)
    reorder_point: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))


class ManufacturingEnergySample(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_energy_samples"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "facility_code"],
            ["manufacturing_facilities.tenant_id", "manufacturing_facilities.facility_code"],
            name="fk_mfg_energy_facility_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_mfg_energy_tenant_facility_time", "tenant_id", "facility_code", "observed_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    facility_code: Mapped[str] = mapped_column(String(64), nullable=False)
    meter_code: Mapped[str] = mapped_column(String(64), nullable=False)
    energy_type: Mapped[str] = mapped_column(String(32), nullable=False)
    consumption: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(24), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
