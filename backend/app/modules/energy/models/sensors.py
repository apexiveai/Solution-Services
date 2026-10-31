
import uuid

from sqlalchemy import (
    CheckConstraint,
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


class EnergySensor(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_sensors"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_sensor_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "sensor_code",
            name="uq_energy_sensor_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_sensor_asset_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_sensor_tenant_asset",
            "tenant_id",
            "asset_id",
        ),
        Index(
            "ix_energy_sensor_tenant_type",
            "tenant_id",
            "sensor_type",
        ),
        Index(
            "ix_energy_sensor_tenant_status",
            "tenant_id",
            "status",
        ),
        CheckConstraint(
            "sampling_interval_seconds > 0",
            name="ck_energy_sensor_sampling_interval",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    sensor_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    sensor_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    measurement_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    measurement_unit: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    sampling_interval_seconds: Mapped[int] = mapped_column(
        nullable=False,
        default=60,
    )

    protocol: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    external_sensor_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    location_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    operational_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="UNKNOWN",
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ACTIVE",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
