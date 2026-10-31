
import uuid

from sqlalchemy import (
    JSON,
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


class EnergyTenantSettings(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_tenant_settings"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            name="uq_energy_tenant_settings_tenant",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    default_timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
    )

    default_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
    )

    monitoring_enabled: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    alarm_enabled: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    visual_inspection_enabled: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    predictive_maintenance_enabled: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    telemetry_retention_days: Mapped[int] = mapped_column(
        nullable=False,
        default=365,
    )

    monitoring_configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    notification_configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    feature_configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
