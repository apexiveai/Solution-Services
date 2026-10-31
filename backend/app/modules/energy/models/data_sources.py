
import uuid

from sqlalchemy import (
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


class EnergyDataSource(
    EnergyTenantMixin,
    EnergyTimestampMixin,
    Base,
):
    __tablename__ = "energy_data_sources"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_energy_data_source_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "source_code",
            name="uq_energy_data_source_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "facility_id"],
            [
                "energy_facilities.tenant_id",
                "energy_facilities.id",
            ],
            name="fk_energy_data_source_facility_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_energy_data_source_tenant_facility",
            "tenant_id",
            "facility_id",
        ),
        Index(
            "ix_energy_data_source_tenant_protocol",
            "tenant_id",
            "protocol",
        ),
        Index(
            "ix_energy_data_source_tenant_status",
            "tenant_id",
            "status",
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

    source_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    protocol: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    endpoint_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    collector_identifier: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    connection_status: Mapped[str] = mapped_column(
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
