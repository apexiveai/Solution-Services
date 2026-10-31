import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
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


class ManufacturingDataSource(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_data_sources"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_mfg_source_tenant_id"),
        UniqueConstraint("tenant_id", "source_code", name="uq_mfg_source_tenant_code"),
        ForeignKeyConstraint(
            ["tenant_id", "equipment_code"],
            ["manufacturing_equipment.tenant_id", "manufacturing_equipment.equipment_code"],
            name="fk_mfg_source_equipment_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_source_tenant_type", "tenant_id", "source_type"),
        Index("ix_mfg_source_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_type: Mapped[str] = mapped_column(String(48), nullable=False)
    protocol: Mapped[str | None] = mapped_column(String(48), nullable=True)
    equipment_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="CONFIGURED")
    configuration: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class ManufacturingMetricSample(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_metric_samples"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "source_code"],
            ["manufacturing_data_sources.tenant_id", "manufacturing_data_sources.source_code"],
            name="fk_mfg_sample_source_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "equipment_code"],
            ["manufacturing_equipment.tenant_id", "manufacturing_equipment.equipment_code"],
            name="fk_mfg_sample_equipment_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_sample_tenant_equipment_time", "tenant_id", "equipment_code", "observed_at"),
        Index("ix_mfg_sample_tenant_metric_time", "tenant_id", "metric_name", "observed_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_code: Mapped[str] = mapped_column(String(64), nullable=False)
    equipment_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    metric_name: Mapped[str] = mapped_column(String(96), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    quality_code: Mapped[str] = mapped_column(String(24), nullable=False, default="GOOD")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dimensions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
