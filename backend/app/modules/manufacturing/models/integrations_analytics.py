import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, JSON, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.manufacturing.models.common import (
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
)


class ManufacturingIntegration(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_integrations"
    __table_args__ = (
        Index("ix_mfg_integration_tenant_type", "tenant_id", "integration_type"),
        Index("ix_mfg_integration_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    integration_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    integration_type: Mapped[str] = mapped_column(String(48), nullable=False)
    direction: Mapped[str] = mapped_column(String(24), nullable=False, default="BIDIRECTIONAL")
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="CONFIGURED")
    configuration: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ManufacturingKPI(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_kpis"
    __table_args__ = (
        Index("ix_mfg_kpi_tenant_code_time", "tenant_id", "kpi_code", "observed_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    kpi_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    target: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    facility_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dimensions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
