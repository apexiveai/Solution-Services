import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.products.catalog import PRODUCT_BY_CODE, PRODUCT_CATALOG
from app.modules.products.models import ProductDeployment
from app.modules.products.schemas import (
    DeploymentStatus,
    ProductDeploymentCreate,
    ProductDeploymentRead,
    ProductDeploymentUpdate,
)
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


def _tenant_id(principal: CurrentPrincipal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token contains an invalid tenant_id claim",
        ) from exc


def _get_deployment(
    db: Session,
    deployment_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> ProductDeployment:
    deployment = db.scalar(
        select(ProductDeployment).where(
            ProductDeployment.id == deployment_id,
            ProductDeployment.tenant_id == tenant_id,
        )
    )
    if deployment is None:
        raise HTTPException(status_code=404, detail="Product deployment not found")
    return deployment


@router.get("/catalog")
def get_catalog(_: CurrentPrincipal = Depends(get_current_principal)) -> dict:
    return {"products": PRODUCT_CATALOG}


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = _tenant_id(principal)
    deployments_by_status = db.execute(
        select(ProductDeployment.status, func.count(ProductDeployment.id))
        .where(ProductDeployment.tenant_id == tenant_id)
        .group_by(ProductDeployment.status)
    ).all()
    deployments_by_product = db.execute(
        select(ProductDeployment.product_code, func.count(ProductDeployment.id))
        .where(ProductDeployment.tenant_id == tenant_id)
        .group_by(ProductDeployment.product_code)
    ).all()
    return {
        "products": len(PRODUCT_CATALOG),
        "deployments": sum(count for _, count in deployments_by_status),
        "deployments_by_status": dict(deployments_by_status),
        "deployments_by_product": dict(deployments_by_product),
    }


@router.post(
    "/deployments",
    response_model=ProductDeploymentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_deployment(
    payload: ProductDeploymentCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ProductDeployment:
    if payload.product_code not in PRODUCT_BY_CODE:
        raise HTTPException(status_code=422, detail="Unknown product_code")

    deployment = ProductDeployment(
        tenant_id=_tenant_id(principal),
        **payload.model_dump(),
    )
    db.add(deployment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A deployment with this name already exists for the tenant",
        ) from exc
    db.refresh(deployment)
    return deployment


@router.get("/deployments", response_model=list[ProductDeploymentRead])
def list_deployments(
    product_code: str | None = Query(default=None, max_length=80),
    deployment_status: DeploymentStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ProductDeployment]:
    tenant_id = _tenant_id(principal)
    statement = select(ProductDeployment).where(ProductDeployment.tenant_id == tenant_id)
    if product_code is not None:
        if product_code not in PRODUCT_BY_CODE:
            raise HTTPException(status_code=422, detail="Unknown product_code")
        statement = statement.where(ProductDeployment.product_code == product_code)
    if deployment_status is not None:
        statement = statement.where(ProductDeployment.status == deployment_status)
    return list(
        db.scalars(
            statement.order_by(ProductDeployment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.get("/deployments/{deployment_id}", response_model=ProductDeploymentRead)
def get_deployment(
    deployment_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ProductDeployment:
    return _get_deployment(db, deployment_id, _tenant_id(principal))


@router.patch("/deployments/{deployment_id}", response_model=ProductDeploymentRead)
def update_deployment(
    deployment_id: uuid.UUID,
    payload: ProductDeploymentUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ProductDeployment:
    updates = payload.model_dump(exclude_unset=True)
    if not updates or any(value is None for value in updates.values()):
        raise HTTPException(status_code=422, detail="Provide at least one non-null field to update")

    deployment = _get_deployment(db, deployment_id, _tenant_id(principal))
    for field, value in updates.items():
        setattr(deployment, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A deployment with this name already exists for the tenant",
        ) from exc
    db.refresh(deployment)
    return deployment
