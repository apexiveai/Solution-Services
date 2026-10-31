import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
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


class ManufacturingSupplier(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_suppliers"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_mfg_supplier_tenant_id"),
        UniqueConstraint("tenant_id", "supplier_code", name="uq_mfg_supplier_tenant_code"),
        Index("ix_mfg_supplier_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    supplier_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    supplier_type: Mapped[str] = mapped_column(String(48), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    contact_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    performance: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class ManufacturingPurchaseOrder(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_purchase_orders"
    __table_args__ = (
        UniqueConstraint("tenant_id", "order_number", name="uq_mfg_purchase_tenant_number"),
        ForeignKeyConstraint(
            ["tenant_id", "supplier_code"],
            ["manufacturing_suppliers.tenant_id", "manufacturing_suppliers.supplier_code"],
            name="fk_mfg_purchase_supplier_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_purchase_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    supplier_code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="DRAFT")
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    expected_delivery: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    total_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    line_items: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
