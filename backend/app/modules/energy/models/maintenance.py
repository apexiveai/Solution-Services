
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


class EnergyMaintenanceWorkOrder(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_maintenance_work_orders"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_work_order_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "work_order_number",
            name="uq_energy_work_order_tenant_number",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_work_order_facility_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_work_order_asset_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "incident_id"],
            [
                "energy_incidents.tenant_id",
                "energy_incidents.id",
            ],
            name="fk_energy_work_order_incident_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_work_order_tenant_status",
            "tenant_id",
            "status",
        ),
        Index(
            "ix_energy_work_order_tenant_asset",
            "tenant_id",
            "asset_id",
        ),
        Index(
            "ix_energy_work_order_tenant_due",
            "tenant_id",
            "scheduled_at",
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

    incident_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    work_order_number: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    maintenance_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="MEDIUM",
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="PLANNED",
    )

    assigned_team: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    assigned_to: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completion_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parts_and_materials: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
