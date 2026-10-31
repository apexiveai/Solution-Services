import uuid

from datetime import datetime
from sqlalchemy import (
    ForeignKeyConstraint,
    Index,
    JSON,
    String,
    Text,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.energy.models.common import (
    EnergyTenantMixin,
    EnergyTimestampMixin,
)


class EnergyIntegration(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_integrations"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_integration_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "integration_code",
            name="uq_energy_integration_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_integration_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_integration_tenant_protocol",
            "tenant_id",
            "protocol",
        ),
        Index(
            "ix_energy_integration_tenant_status",
            "tenant_id",
            "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    facility_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    integration_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    integration_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    protocol: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    deployment_mode: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ON_PREMISES",
    )

    endpoint_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    credential_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    capabilities: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    connection_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="UNKNOWN",
    )

    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
