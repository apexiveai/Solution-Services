
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


class EnergyAlarm(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_alarms"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_alarm_tenant_id",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_alarm_facility_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_alarm_asset_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "sensor_id"],
            [
                "energy_sensors.tenant_id",
                "energy_sensors.id",
            ],
            name="fk_energy_alarm_sensor_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_alarm_tenant_status_severity",
            "tenant_id",
            "status",
            "severity",
        ),
        Index(
            "ix_energy_alarm_tenant_facility_time",
            "tenant_id",
            "facility_id",
            "occurred_at",
        ),
        Index(
            "ix_energy_alarm_tenant_asset",
            "tenant_id",
            "asset_id",
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

    sensor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    alarm_code: Mapped[str] = mapped_column(
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

    alarm_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="WARNING",
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="OPEN",
    )

    source_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    measured_value: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    threshold_value: Mapped[str | None] = mapped_column(
        String(80),
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

    acknowledged_by: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_by: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
