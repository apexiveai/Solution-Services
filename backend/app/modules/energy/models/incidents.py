
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


class EnergyIncident(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_incidents"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_incident_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "incident_number",
            name="uq_energy_incident_tenant_number",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_incident_facility_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_incident_asset_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "alarm_id"],
            [
                "energy_alarms.tenant_id",
                "energy_alarms.id",
            ],
            name="fk_energy_incident_alarm_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_incident_tenant_status_priority",
            "tenant_id",
            "status",
            "priority",
        ),
        Index(
            "ix_energy_incident_tenant_facility",
            "tenant_id",
            "facility_id",
        ),
        Index(
            "ix_energy_incident_tenant_created",
            "tenant_id",
            "created_at",
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

    alarm_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    incident_number: Mapped[str] = mapped_column(
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

    incident_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="MEDIUM",
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="OPEN",
    )

    impact_level: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="UNKNOWN",
    )

    assigned_team: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    assigned_to: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    root_cause: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    resolution_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
