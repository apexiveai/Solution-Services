import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.manufacturing.models.common import (
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
)


class ManufacturingQualityInspection(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_quality_inspections"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "order_number"],
            ["manufacturing_production_orders.tenant_id", "manufacturing_production_orders.order_number"],
            name="fk_mfg_quality_order_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_mfg_quality_tenant_order", "tenant_id", "order_number"),
        Index("ix_mfg_quality_tenant_status", "tenant_id", "status"),
        CheckConstraint("sample_size >= 1", name="ck_mfg_quality_sample_size"),
        CheckConstraint(
            "defect_count >= 0 AND defect_count <= sample_size",
            name="ck_mfg_quality_defect_count",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    product_code: Mapped[str] = mapped_column(String(64), nullable=False)
    inspection_type: Mapped[str] = mapped_column(String(48), nullable=False)
    sample_size: Mapped[int] = mapped_column(nullable=False, default=1)
    defect_count: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="PENDING")
    inspector_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    findings: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    inspected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ManufacturingMaintenancePrediction(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_maintenance_predictions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "equipment_code"],
            ["manufacturing_equipment.tenant_id", "manufacturing_equipment.equipment_code"],
            name="fk_mfg_prediction_equipment_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_mfg_prediction_tenant_equipment", "tenant_id", "equipment_code"),
        Index("ix_mfg_prediction_tenant_risk", "tenant_id", "risk_level"),
        CheckConstraint(
            "probability >= 0 AND probability <= 1",
            name="ck_mfg_prediction_probability",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    equipment_code: Mapped[str] = mapped_column(String(64), nullable=False)
    model_name: Mapped[str] = mapped_column(String(96), nullable=False)
    failure_mode: Mapped[str] = mapped_column(String(96), nullable=False)
    probability: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(24), nullable=False)
    predicted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expected_failure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    contributing_signals: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class ManufacturingMaintenanceWorkOrder(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_maintenance_work_orders"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "equipment_code"],
            ["manufacturing_equipment.tenant_id", "manufacturing_equipment.equipment_code"],
            name="fk_mfg_work_order_equipment_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_work_order_tenant_status", "tenant_id", "status"),
        Index("ix_mfg_work_order_tenant_equipment", "tenant_id", "equipment_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    work_order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    equipment_code: Mapped[str] = mapped_column(String(64), nullable=False)
    work_type: Mapped[str] = mapped_column(String(40), nullable=False)
    priority: Mapped[str] = mapped_column(String(24), nullable=False, default="NORMAL")
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="OPEN")
    assigned_to: Mapped[str | None] = mapped_column(String(128), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
