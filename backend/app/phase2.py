
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    or_,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base, get_db


# ============================================================
# APEXIVEAI ENTERPRISE OPERATIONS PLATFORM
# PHASE 2 - ADMINISTRATION & TENANT MANAGEMENT
# ============================================================

router = APIRouter(
    prefix="/api/v1/phase2",
    tags=["AEOP Phase 2"],
)

security = HTTPBearer(auto_error=True)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================
# AUTHENTICATION & AUTHORIZATION
# ============================================================

def get_jwt_claims(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:

    jwks_url = os.getenv("AEOP_JWKS_URL", "").strip()
    issuer = os.getenv("AEOP_JWT_ISSUER", "").strip()
    audience = os.getenv("AEOP_JWT_AUDIENCE", "").strip()

    if not jwks_url:
        raise HTTPException(
            status_code=503,
            detail="AEOP_JWKS_URL is not configured",
        )

    try:
        jwks = jwt.PyJWKClient(jwks_url)
        signing_key = jwks.get_signing_key_from_jwt(
            credentials.credentials
        ).key

        claims = jwt.decode(
            credentials.credentials,
            signing_key,
            algorithms=["RS256"],
            issuer=issuer if issuer else None,
            audience=audience if audience else None,
            options={
                "verify_iss": bool(issuer),
                "verify_aud": bool(audience),
                "require": ["exp", "sub"],
            },
        )

        return claims

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        ) from exc


def extract_roles(claims: dict[str, Any]) -> set[str]:

    roles = set(claims.get("roles") or [])

    realm_access = claims.get("realm_access") or {}
    roles.update(realm_access.get("roles") or [])

    resource_access = claims.get("resource_access") or {}

    if isinstance(resource_access, dict):
        for client in resource_access.values():
            if isinstance(client, dict):
                roles.update(client.get("roles") or [])

    return {
        str(role).strip().upper()
        for role in roles
    }


def require_super_admin(
    claims: dict[str, Any] = Depends(get_jwt_claims),
) -> dict[str, Any]:

    allowed_roles = {
        "SUPER_ADMIN",
        "SUPER-ADMIN",
        "SUPER_ADMINISTRATOR",
    }

    if not extract_roles(claims).intersection(allowed_roles):
        raise HTTPException(
            status_code=403,
            detail="Super Admin permission required",
        )

    return claims


# ============================================================
# DATABASE MODELS
# ============================================================

class Tenant(Base):

    __tablename__ = "aeop_tenants"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_aeop_tenant_code",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    code: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class Product(Base):

    __tablename__ = "aeop_products"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_aeop_product_code",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    version: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="1.0.0",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class TenantLicense(Base):

    __tablename__ = "aeop_tenant_licenses"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "product_id",
            name="uq_aeop_tenant_product_license",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("aeop_tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("aeop_products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
        index=True,
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class Subscription(Base):

    __tablename__ = "aeop_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("aeop_tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    plan_code: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
        index=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="MMK",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
    )

    starts_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class PlatformUser(Base):

    __tablename__ = "aeop_platform_users"

    __table_args__ = (
        UniqueConstraint(
            "identity_subject",
            name="uq_aeop_identity_subject",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("aeop_tenants.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    identity_subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    display_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    role: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="TENANT_USER",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


class AuditEvent(Base):

    __tablename__ = "aeop_audit_events"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    actor_subject: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resource_type: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    tenant_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    detail: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True,
    )


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TenantCreate(BaseModel):

    code: str = Field(
        min_length=2,
        max_length=60,
        pattern=r"^[A-Za-z0-9_-]+$",
    )

    name: str = Field(
        min_length=2,
        max_length=200,
    )

    legal_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None


class TenantUpdate(BaseModel):

    name: str | None = Field(default=None, min_length=2, max_length=200)
    legal_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    status: str | None = Field(
        default=None,
        pattern=r"^(ACTIVE|SUSPENDED)$",
    )


class TenantResponse(ORMBase):

    id: uuid.UUID
    code: str
    name: str
    legal_name: str | None
    contact_email: str | None
    contact_phone: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):

    code: str = Field(
        min_length=2,
        max_length=80,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )

    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    version: str = "1.0.0"


class ProductResponse(ORMBase):

    id: uuid.UUID
    code: str
    name: str
    description: str | None
    version: str
    is_active: bool
    created_at: datetime


class LicenseCreate(BaseModel):

    product_id: uuid.UUID
    starts_at: datetime | None = None
    expires_at: datetime | None = None
    seats: int = Field(default=1, ge=1, le=100000)


class SubscriptionCreate(BaseModel):

    plan_code: str = Field(min_length=2, max_length=60)
    currency: str = Field(default="MMK", min_length=3, max_length=3)
    amount: Decimal = Field(default=Decimal("0"), ge=0)
    starts_at: datetime | None = None
    ends_at: datetime | None = None


class TenantUserCreate(BaseModel):

    identity_subject: str = Field(min_length=3, max_length=255)
    email: str | None = None
    display_name: str | None = None
    role: str = Field(
        default="TENANT_USER",
        pattern=r"^(TENANT_ADMIN|TENANT_USER|TENANT_VIEWER)$",
    )


# ============================================================
# HELPERS
# ============================================================

def write_audit(
    db: Session,
    claims: dict,
    action: str,
    resource_type: str,
    resource_id: Any = None,
    tenant_id: uuid.UUID | None = None,
):
    event = AuditEvent(
        actor_subject=str(claims.get("sub", "")),
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id else None,
        tenant_id=tenant_id,
    )

    db.add(event)


def get_tenant_or_404(
    db: Session,
    tenant_id: uuid.UUID,
) -> Tenant:

    tenant = db.get(Tenant, tenant_id)

    if tenant is None:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found",
        )

    return tenant


# ============================================================
# SUPER ADMIN DASHBOARD
# ============================================================

@router.get("/dashboard")
def get_dashboard(
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    now = utc_now()

    return {
        "tenants_total": db.query(func.count(Tenant.id)).scalar() or 0,

        "tenants_active": (
            db.query(func.count(Tenant.id))
            .filter(Tenant.status == "ACTIVE")
            .scalar() or 0
        ),

        "tenants_suspended": (
            db.query(func.count(Tenant.id))
            .filter(Tenant.status == "SUSPENDED")
            .scalar() or 0
        ),

        "products_total": (
            db.query(func.count(Product.id)).scalar() or 0
        ),

        "active_licenses": (
            db.query(func.count(TenantLicense.id))
            .filter(
                TenantLicense.status == "ACTIVE",
                or_(
                    TenantLicense.expires_at.is_(None),
                    TenantLicense.expires_at > now,
                ),
            )
            .scalar() or 0
        ),

        "pending_subscriptions": (
            db.query(func.count(Subscription.id))
            .filter(Subscription.status == "PENDING")
            .scalar() or 0
        ),

        "generated_at": now,
    }


# ============================================================
# TENANT MANAGEMENT
# ============================================================

@router.get(
    "/tenants",
    response_model=list[TenantResponse],
)
def list_tenants(
    search: str | None = None,
    tenant_status: str | None = Query(
        default=None,
        alias="status",
        pattern=r"^(ACTIVE|SUSPENDED)$",
    ),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    query = db.query(Tenant)

    if search:
        keyword = f"%{search.strip()}%"

        query = query.filter(
            or_(
                Tenant.name.ilike(keyword),
                Tenant.code.ilike(keyword),
                Tenant.legal_name.ilike(keyword),
            )
        )

    if tenant_status:
        query = query.filter(Tenant.status == tenant_status)

    return (
        query
        .order_by(Tenant.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.post(
    "/tenants",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tenant(
    payload: TenantCreate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    code = payload.code.strip().upper()

    exists = (
        db.query(Tenant)
        .filter(Tenant.code == code)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=409,
            detail="Tenant code already exists",
        )

    tenant = Tenant(
        code=code,
        name=payload.name.strip(),
        legal_name=payload.legal_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
        status="ACTIVE",
    )

    try:
        db.add(tenant)
        db.flush()

        write_audit(
            db,
            claims,
            "tenant.created",
            "tenant",
            tenant.id,
            tenant.id,
        )

        db.commit()
        db.refresh(tenant)

        return tenant

    except Exception:
        db.rollback()
        raise


@router.get(
    "/tenants/{tenant_id}",
    response_model=TenantResponse,
)
def get_tenant(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    return get_tenant_or_404(db, tenant_id)


@router.patch(
    "/tenants/{tenant_id}",
    response_model=TenantResponse,
)
def update_tenant(
    tenant_id: uuid.UUID,
    payload: TenantUpdate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    tenant = get_tenant_or_404(db, tenant_id)

    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():

        if value is not None:
            setattr(
                tenant,
                field,
                value.strip() if isinstance(value, str) else value,
            )

    write_audit(
        db,
        claims,
        "tenant.updated",
        "tenant",
        tenant.id,
        tenant.id,
    )

    db.commit()
    db.refresh(tenant)

    return tenant


@router.post(
    "/tenants/{tenant_id}/suspend",
    response_model=TenantResponse,
)
def suspend_tenant(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    tenant = get_tenant_or_404(db, tenant_id)

    tenant.status = "SUSPENDED"

    write_audit(
        db,
        claims,
        "tenant.suspended",
        "tenant",
        tenant.id,
        tenant.id,
    )

    db.commit()
    db.refresh(tenant)

    return tenant


@router.post(
    "/tenants/{tenant_id}/activate",
    response_model=TenantResponse,
)
def activate_tenant(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    tenant = get_tenant_or_404(db, tenant_id)

    tenant.status = "ACTIVE"

    write_audit(
        db,
        claims,
        "tenant.activated",
        "tenant",
        tenant.id,
        tenant.id,
    )

    db.commit()
    db.refresh(tenant)

    return tenant


# ============================================================
# PRODUCT / SOLUTION CATALOG
# ============================================================

@router.get(
    "/products",
    response_model=list[ProductResponse],
)
def list_products(
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    return (
        db.query(Product)
        .order_by(Product.name.asc())
        .all()
    )


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    code = payload.code.strip().upper()

    if db.query(Product).filter(Product.code == code).first():
        raise HTTPException(
            status_code=409,
            detail="Product code already exists",
        )

    product = Product(
        code=code,
        name=payload.name.strip(),
        description=payload.description,
        version=payload.version,
        is_active=True,
    )

    db.add(product)
    db.flush()

    write_audit(
        db,
        claims,
        "product.created",
        "product",
        product.id,
    )

    db.commit()
    db.refresh(product)

    return product


@router.post("/products/{product_id}/deactivate")
def deactivate_product(
    product_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    product.is_active = False

    write_audit(
        db,
        claims,
        "product.deactivated",
        "product",
        product.id,
    )

    db.commit()

    return {
        "id": str(product.id),
        "status": "DEACTIVATED",
    }


# ============================================================
# TENANT PRODUCT LICENSES
# ============================================================

@router.post(
    "/tenants/{tenant_id}/licenses",
    status_code=status.HTTP_201_CREATED,
)
def assign_license(
    tenant_id: uuid.UUID,
    payload: LicenseCreate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    tenant = get_tenant_or_404(db, tenant_id)

    if tenant.status != "ACTIVE":
        raise HTTPException(
            status_code=409,
            detail="Cannot assign license to suspended tenant",
        )

    product = db.get(Product, payload.product_id)

    if product is None or not product.is_active:
        raise HTTPException(
            status_code=404,
            detail="Active product not found",
        )

    if (
        payload.starts_at
        and payload.expires_at
        and payload.expires_at <= payload.starts_at
    ):
        raise HTTPException(
            status_code=422,
            detail="Expiration must be later than start date",
        )

    existing = (
        db.query(TenantLicense)
        .filter(
            TenantLicense.tenant_id == tenant_id,
            TenantLicense.product_id == payload.product_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="A license record already exists for this product and tenant",
        )

    license_record = TenantLicense(
        tenant_id=tenant_id,
        product_id=payload.product_id,
        starts_at=payload.starts_at or utc_now(),
        expires_at=payload.expires_at,
        seats=payload.seats,
        status="ACTIVE",
    )

    db.add(license_record)
    db.flush()

    write_audit(
        db,
        claims,
        "license.assigned",
        "license",
        license_record.id,
        tenant_id,
    )

    db.commit()
    db.refresh(license_record)

    return {
        "id": str(license_record.id),
        "tenant_id": str(license_record.tenant_id),
        "product_id": str(license_record.product_id),
        "status": license_record.status,
        "starts_at": license_record.starts_at,
        "expires_at": license_record.expires_at,
        "seats": license_record.seats,
    }


@router.get("/tenants/{tenant_id}/licenses")
def list_tenant_licenses(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    get_tenant_or_404(db, tenant_id)

    rows = (
        db.query(TenantLicense, Product)
        .join(Product, Product.id == TenantLicense.product_id)
        .filter(TenantLicense.tenant_id == tenant_id)
        .order_by(TenantLicense.created_at.desc())
        .all()
    )

    return [
        {
            "id": str(license_record.id),
            "product_code": product.code,
            "product_name": product.name,
            "status": license_record.status,
            "starts_at": license_record.starts_at,
            "expires_at": license_record.expires_at,
            "seats": license_record.seats,
        }
        for license_record, product in rows
    ]


@router.post("/licenses/{license_id}/revoke")
def revoke_license(
    license_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    license_record = db.get(TenantLicense, license_id)

    if license_record is None:
        raise HTTPException(
            status_code=404,
            detail="License not found",
        )

    license_record.status = "REVOKED"

    write_audit(
        db,
        claims,
        "license.revoked",
        "license",
        license_record.id,
        license_record.tenant_id,
    )

    db.commit()

    return {
        "id": str(license_record.id),
        "status": "REVOKED",
    }


# ============================================================
# SUBSCRIPTION MANAGEMENT
# ============================================================

@router.post(
    "/tenants/{tenant_id}/subscriptions",
    status_code=status.HTTP_201_CREATED,
)
def create_subscription(
    tenant_id: uuid.UUID,
    payload: SubscriptionCreate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    get_tenant_or_404(db, tenant_id)

    if (
        payload.starts_at
        and payload.ends_at
        and payload.ends_at <= payload.starts_at
    ):
        raise HTTPException(
            status_code=422,
            detail="End date must be later than start date",
        )

    subscription = Subscription(
        tenant_id=tenant_id,
        plan_code=payload.plan_code.strip().upper(),
        currency=payload.currency.upper(),
        amount=payload.amount,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        status="PENDING",
    )

    db.add(subscription)
    db.flush()

    write_audit(
        db,
        claims,
        "subscription.created",
        "subscription",
        subscription.id,
        tenant_id,
    )

    db.commit()
    db.refresh(subscription)

    return {
        "id": str(subscription.id),
        "tenant_id": str(subscription.tenant_id),
        "plan_code": subscription.plan_code,
        "status": subscription.status,
        "currency": subscription.currency,
        "amount": str(subscription.amount),
        "starts_at": subscription.starts_at,
        "ends_at": subscription.ends_at,
    }


@router.get("/tenants/{tenant_id}/subscriptions")
def list_subscriptions(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    get_tenant_or_404(db, tenant_id)

    rows = (
        db.query(Subscription)
        .filter(Subscription.tenant_id == tenant_id)
        .order_by(Subscription.created_at.desc())
        .all()
    )

    return [
        {
            "id": str(item.id),
            "plan_code": item.plan_code,
            "status": item.status,
            "currency": item.currency,
            "amount": str(item.amount),
            "starts_at": item.starts_at,
            "ends_at": item.ends_at,
        }
        for item in rows
    ]


@router.post("/subscriptions/{subscription_id}/activate")
def activate_subscription(
    subscription_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    subscription = db.get(Subscription, subscription_id)

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    subscription.status = "ACTIVE"

    write_audit(
        db,
        claims,
        "subscription.activated",
        "subscription",
        subscription.id,
        subscription.tenant_id,
    )

    db.commit()

    return {
        "id": str(subscription.id),
        "status": "ACTIVE",
    }


# ============================================================
# TENANT USER MANAGEMENT
# ============================================================

@router.post(
    "/tenants/{tenant_id}/users",
    status_code=status.HTTP_201_CREATED,
)
def create_tenant_user(
    tenant_id: uuid.UUID,
    payload: TenantUserCreate,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    tenant = get_tenant_or_404(db, tenant_id)

    if tenant.status != "ACTIVE":
        raise HTTPException(
            status_code=409,
            detail="Cannot add users to a suspended tenant",
        )

    subject = payload.identity_subject.strip()

    exists = (
        db.query(PlatformUser)
        .filter(PlatformUser.identity_subject == subject)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=409,
            detail="Identity subject is already registered",
        )

    user = PlatformUser(
        tenant_id=tenant_id,
        identity_subject=subject,
        email=payload.email,
        display_name=payload.display_name,
        role=payload.role,
        status="ACTIVE",
    )

    db.add(user)
    db.flush()

    write_audit(
        db,
        claims,
        "tenant_user.created",
        "platform_user",
        user.id,
        tenant_id,
    )

    db.commit()
    db.refresh(user)

    return {
        "id": str(user.id),
        "tenant_id": str(user.tenant_id),
        "identity_subject": user.identity_subject,
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role,
        "status": user.status,
    }


@router.get("/tenants/{tenant_id}/users")
def list_tenant_users(
    tenant_id: uuid.UUID,
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    get_tenant_or_404(db, tenant_id)

    users = (
        db.query(PlatformUser)
        .filter(PlatformUser.tenant_id == tenant_id)
        .order_by(PlatformUser.created_at.desc())
        .all()
    )

    return [
        {
            "id": str(user.id),
            "identity_subject": user.identity_subject,
            "email": user.email,
            "display_name": user.display_name,
            "role": user.role,
            "status": user.status,
        }
        for user in users
    ]


# ============================================================
# AUDIT LOGS
# ============================================================

@router.get("/audit")
def list_audit_events(
    tenant_id: uuid.UUID | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    claims: dict = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    query = db.query(AuditEvent)

    if tenant_id:
        query = query.filter(
            AuditEvent.tenant_id == tenant_id
        )

    events = (
        query
        .order_by(AuditEvent.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": str(event.id),
            "actor_subject": event.actor_subject,
            "action": event.action,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "tenant_id": (
                str(event.tenant_id)
                if event.tenant_id else None
            ),
            "detail": event.detail,
            "created_at": event.created_at,
        }
        for event in events
    ]


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def phase2_health():

    return {
        "platform": "ApexiveAI Enterprise Operations Platform",
        "module": "Phase 2",
        "status": "READY",
        "timestamp": utc_now(),
    }
