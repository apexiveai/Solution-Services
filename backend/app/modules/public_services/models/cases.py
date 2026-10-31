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
from app.modules.public_services.models.common import (
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
)


class PublicServiceDefinition(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_service_definitions"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "service_code",
            name="uq_public_service_tenant_code",
        ),
        Index("ix_public_service_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    service_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="ONLINE")
    sla_hours: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="ACTIVE")
    requirements: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicServiceCase(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_service_cases"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_public_case_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "case_number",
            name="uq_public_case_tenant_number",
        ),
        Index("ix_public_case_tenant_status", "tenant_id", "status"),
        Index("ix_public_case_tenant_created", "tenant_id", "created_at"),
        Index("ix_public_case_tenant_assignee", "tenant_id", "assigned_to"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    case_number: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    service_code: Mapped[str] = mapped_column(String(64), nullable=False)
    requester_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    subject: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="SUBMITTED")
    priority: Mapped[str] = mapped_column(String(24), nullable=False, default="NORMAL")
    assigned_to: Mapped[str | None] = mapped_column(String(128), nullable=True)
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class PublicServiceInteraction(
    PublicServicesTenantMixin,
    PublicServicesTimestampMixin,
    Base,
):
    __tablename__ = "public_service_interactions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "case_id"],
            ["public_service_cases.tenant_id", "public_service_cases.id"],
            name="fk_public_interaction_case_tenant",
            ondelete="CASCADE",
        ),
        Index("ix_public_interaction_tenant_case", "tenant_id", "case_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    actor_reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
