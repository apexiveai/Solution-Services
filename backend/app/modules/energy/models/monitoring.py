
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
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.energy.models.common import (
    EnergyTenantMixin,
    EnergyTimestampMixin,
)


class EnergyMetricSample(
    EnergyTenantMixin,
    Base,
):
    __tablename__ = "energy_metric_samples"

    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "sensor_id"],
            [
                "energy_sensors.tenant_id",
                "energy_sensors.id",
            ],
            name="fk_energy_metric_sensor_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "asset_id"],
            [
                "energy_assets.tenant_id",
                "energy_assets.id",
            ],
            name="fk_energy_metric_asset_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "data_source_id"],
            [
                "energy_data_sources.tenant_id",
                "energy_data_sources.id",
            ],
            name="fk_energy_metric_source_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_metric_tenant_sensor_time",
            "tenant_id",
            "sensor_id",
            "observed_at",
        ),
        Index(
            "ix_energy_metric_tenant_asset_time",
            "tenant_id",
            "asset_id",
            "observed_at",
        ),
        Index(
            "ix_energy_metric_tenant_time",
            "tenant_id",
            "observed_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    sensor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    data_source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    metric_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    metric_value: Mapped[Decimal] = mapped_column(
        Numeric(24, 8),
        nullable=False,
    )

    measurement_unit: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    quality_status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="GOOD",
    )

    sequence_number: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
