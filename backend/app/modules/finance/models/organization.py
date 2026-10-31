
import uuid

from sqlalchemy import (
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.finance.models.common import (
    FinanceTenantMixin,
    FinanceTimestampMixin,
)


class FinanceInstitution(
    FinanceTenantMixin,
    FinanceTimestampMixin,
    Base,
):
    __tablename__ = "finance_institutions"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_fin_institution_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "institution_code",
            name="uq_fin_institution_tenant_code",
        ),
        Index(
            "ix_fin_institution_tenant_status",
            "tenant_id",
            "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    institution_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    institution_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        index=True,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    base_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
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


class FinanceBranch(
    FinanceTenantMixin,
    FinanceTimestampMixin,
    Base,
):
    __tablename__ = "finance_branches"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_fin_branch_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "branch_code",
            name="uq_fin_branch_tenant_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "institution_id"],
            [
                "finance_institutions.tenant_id",
                "finance_institutions.id",
            ],
            name="fk_fin_branch_institution_tenant",
            ondelete="CASCADE",
        ),
        Index(
            "ix_fin_branch_tenant_institution",
            "tenant_id",
            "institution_id",
        ),
        Index(
            "ix_fin_branch_tenant_status",
            "tenant_id",
            "status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    branch_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    branch_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="BRANCH",
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ACTIVE",
    )
