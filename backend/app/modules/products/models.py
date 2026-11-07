import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ProductDeployment(Base):
    __tablename__ = "product_deployments"
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_product_deployments_tenant_name"),
        CheckConstraint(
            "status IN ('PLANNED', 'ACTIVE', 'PAUSED', 'RETIRED')",
            name="ck_product_deployments_status",
        ),
        CheckConstraint(
            "environment IN ('DEVELOPMENT', 'STAGING', 'PRODUCTION')",
            name="ck_product_deployments_environment",
        ),
        Index("ix_product_deployments_tenant_status", "tenant_id", "status"),
        Index("ix_product_deployments_tenant_product", "tenant_id", "product_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_code: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    environment: Mapped[str] = mapped_column(String(24), nullable=False, default="DEVELOPMENT")
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="PLANNED")
    configuration: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    integrations: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
