import uuid

from sqlalchemy import (
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


class ManufacturingFacility(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_facilities"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_mfg_facility_tenant_id"),
        UniqueConstraint("tenant_id", "facility_code", name="uq_mfg_facility_tenant_code"),
        Index("ix_mfg_facility_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    facility_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    facility_type: Mapped[str] = mapped_column(String(48), nullable=False, default="FACTORY")
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")


class ManufacturingEquipment(
    ManufacturingTenantMixin,
    ManufacturingTimestampMixin,
    Base,
):
    __tablename__ = "manufacturing_equipment"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_mfg_equipment_tenant_id"),
        UniqueConstraint("tenant_id", "equipment_code", name="uq_mfg_equipment_tenant_code"),
        ForeignKeyConstraint(
            ["tenant_id", "facility_code"],
            ["manufacturing_facilities.tenant_id", "manufacturing_facilities.facility_code"],
            name="fk_mfg_equipment_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index("ix_mfg_equipment_tenant_status", "tenant_id", "status"),
        Index("ix_mfg_equipment_tenant_line", "tenant_id", "production_line"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    equipment_code: Mapped[str] = mapped_column(String(64), nullable=False)
    facility_code: Mapped[str] = mapped_column(String(64), nullable=False)
    production_line: Mapped[str | None] = mapped_column(String(96), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    equipment_type: Mapped[str] = mapped_column(String(64), nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String(150), nullable=True)
    model_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="UNKNOWN")
    criticality: Mapped[str] = mapped_column(String(24), nullable=False, default="MEDIUM")
    rated_capacity: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    properties: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
