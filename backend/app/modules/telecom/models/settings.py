
import uuid

from sqlalchemy import JSON, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.telecom.models.common import (
    TelecomTenantMixin,
    TelecomTimestampMixin,
)


class TelecomTenantSetting(
    Base, TelecomTenantMixin, TelecomTimestampMixin
):
    __tablename__ = "telecom_tenant_settings"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "setting_key",
            name="uq_telecom_setting_tenant_key",
        ),
        Index(
            "ix_telecom_settings_tenant_category",
            "tenant_id",
            "category",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    category: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    setting_key: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    setting_value: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
