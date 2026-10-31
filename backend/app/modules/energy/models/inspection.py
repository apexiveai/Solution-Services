import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    JSON,
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


class EnergyInspectionRecord(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_inspection_records"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_inspection_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "inspection_number",
            name="uq_energy_inspection_tenant_number",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_inspection_facility_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_inspection_asset_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_inspection_tenant_facility",
            "tenant_id",
            "facility_id",
        ),
        Index(
            "ix_energy_inspection_tenant_asset",
            "tenant_id",
            "asset_id",
        ),
        Index(
            "ix_energy_inspection_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_energy_inspection_tenant_time",
            "tenant_id",
            "inspected_at",
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

    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    inspection_number: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    inspection_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    inspection_method: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    inspector_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    inspected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="PENDING",
    )

    findings: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    defect_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommended_action: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    evidence_references: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    ai_assessment: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="RECORDED",
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
