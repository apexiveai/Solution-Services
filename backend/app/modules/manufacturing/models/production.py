import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
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
from app.modules.manufacturing.models.common import (
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
)


class ManufacturingProductionOrder(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_production_orders"
    __table_args__ = (
        UniqueConstraint("tenant_id", "order_number", name="uq_mfg_order_tenant_number"),
        ForeignKeyConstraint(
            ["tenant_id", "facility_code"],
            ["manufacturing_facilities.tenant_id", "manufacturing_facilities.facility_code"],
            name="fk_mfg_order_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_order_tenant_status", "tenant_id", "status"),
        Index("ix_mfg_order_tenant_schedule", "tenant_id", "planned_start"),
        CheckConstraint("planned_quantity > 0", name="ck_mfg_order_planned_quantity"),
        CheckConstraint("completed_quantity >= 0", name="ck_mfg_order_completed_quantity"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    product_code: Mapped[str] = mapped_column(String(64), nullable=False)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    facility_code: Mapped[str] = mapped_column(String(64), nullable=False)
    production_line: Mapped[str | None] = mapped_column(String(96), nullable=True)
    planned_quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    completed_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 4), nullable=False, default=0
    )
    unit_of_measure: Mapped[str] = mapped_column(String(24), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PLANNED")
    planned_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    planned_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
