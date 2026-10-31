
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    Numeric,
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


class FinanceProduct(
    FinanceTenantMixin,
    FinanceTimestampMixin,
    Base,
):
    __tablename__ = "finance_products"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_fin_product_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "institution_id",
            "product_code",
            name="uq_fin_product_institution_code",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "institution_id"],
            [
                "finance_institutions.tenant_id",
                "finance_institutions.id",
            ],
            name="fk_fin_product_institution_tenant",
            ondelete="CASCADE",
        ),
        Index(
            "ix_fin_product_tenant_type_status",
            "tenant_id",
            "product_type",
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

    product_code: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    product_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    minimum_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 4),
        nullable=True,
    )

    maximum_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 4),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ACTIVE",
    )


class FinanceAccount(
    FinanceTenantMixin,
    FinanceTimestampMixin,
    Base,
):
    __tablename__ = "finance_accounts"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_fin_account_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "account_reference_token",
            name="uq_fin_account_reference_token",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "institution_id"],
            [
                "finance_institutions.tenant_id",
                "finance_institutions.id",
            ],
            name="fk_fin_account_institution_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "product_id"],
            [
                "finance_products.tenant_id",
                "finance_products.id",
            ],
            name="fk_fin_account_product_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            [
                "finance_branches.tenant_id",
                "finance_branches.id",
            ],
            name="fk_fin_account_branch_tenant",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_fin_account_tenant_institution",
            "tenant_id",
            "institution_id",
        ),
        Index(
            "ix_fin_account_tenant_status",
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

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    account_reference_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    masked_account_reference: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    customer_reference_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    account_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default="ACTIVE",
    )

    opened_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
