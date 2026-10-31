import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.manufacturing.catalog import (
    ARCHITECTURE_LAYERS,
    CAPABILITY_CATALOG,
    MODULE_CATALOG,
)
from app.modules.manufacturing.models import (
    ManufacturingDataSource,
    ManufacturingEquipment,
    ManufacturingFacility,
    ManufacturingMetricSample,
    ManufacturingProductionOrder,
)
from app.modules.manufacturing.schemas import (
    DataSourceCreate,
    DataSourceRead,
    EquipmentCreate,
    EquipmentRead,
    FacilityCreate,
    FacilityRead,
    MetricSampleCreate,
    MetricSampleRead,
    ProductionOrderCreate,
    ProductionOrderRead,
)
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/manufacturing", tags=["Manufacturing"])


def _tenant_id(principal: CurrentPrincipal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token contains an invalid tenant_id claim",
        ) from exc


@router.get("/catalog")
def get_catalog(
    _: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    return {
        "modules": MODULE_CATALOG,
        "capabilities": CAPABILITY_CATALOG,
        "architecture": ARCHITECTURE_LAYERS,
    }


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = _tenant_id(principal)
    order_counts = db.execute(
        select(
            ManufacturingProductionOrder.status,
            func.count(ManufacturingProductionOrder.id),
        )
        .where(ManufacturingProductionOrder.tenant_id == tenant_id)
        .group_by(ManufacturingProductionOrder.status)
    ).all()
    return {
        "modules": MODULE_CATALOG,
        "orders_by_status": dict(order_counts),
        "equipment_count": db.scalar(
            select(func.count(ManufacturingEquipment.id)).where(
                ManufacturingEquipment.tenant_id == tenant_id
            )
        )
        or 0,
        "latest_metrics": db.scalar(
            select(func.count(ManufacturingMetricSample.id)).where(
                ManufacturingMetricSample.tenant_id == tenant_id
            )
        )
        or 0,
    }


@router.post(
    "/facilities",
    response_model=FacilityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_facility(
    payload: FacilityCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ManufacturingFacility:
    facility = ManufacturingFacility(
        tenant_id=_tenant_id(principal),
        **payload.model_dump(),
    )
    db.add(facility)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Facility code already exists") from exc
    db.refresh(facility)
    return facility


@router.get("/facilities", response_model=list[FacilityRead])
def list_facilities(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ManufacturingFacility]:
    tenant_id = _tenant_id(principal)
    return list(
        db.scalars(
            select(ManufacturingFacility)
            .where(ManufacturingFacility.tenant_id == tenant_id)
            .order_by(ManufacturingFacility.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.post(
    "/equipment",
    response_model=EquipmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_equipment(
    payload: EquipmentCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ManufacturingEquipment:
    equipment = ManufacturingEquipment(
        tenant_id=_tenant_id(principal),
        **payload.model_dump(),
    )
    db.add(equipment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Equipment code already exists or facility is invalid",
        ) from exc
    db.refresh(equipment)
    return equipment


@router.get("/equipment", response_model=list[EquipmentRead])
def list_equipment(
    facility_code: str | None = None,
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ManufacturingEquipment]:
    tenant_id = _tenant_id(principal)
    query = select(ManufacturingEquipment).where(
        ManufacturingEquipment.tenant_id == tenant_id
    )
    if facility_code is not None:
        query = query.where(ManufacturingEquipment.facility_code == facility_code)
    return list(
        db.scalars(
            query.order_by(ManufacturingEquipment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.post(
    "/data-sources",
    response_model=DataSourceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_data_source(
    payload: DataSourceCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ManufacturingDataSource:
    source = ManufacturingDataSource(
        tenant_id=_tenant_id(principal),
        **payload.model_dump(),
    )
    db.add(source)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Data source code already exists or equipment is invalid",
        ) from exc
    db.refresh(source)
    return source


@router.get("/data-sources", response_model=list[DataSourceRead])
def list_data_sources(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ManufacturingDataSource]:
    tenant_id = _tenant_id(principal)
    return list(
        db.scalars(
            select(ManufacturingDataSource)
            .where(ManufacturingDataSource.tenant_id == tenant_id)
            .order_by(ManufacturingDataSource.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.post(
    "/production-orders",
    response_model=ProductionOrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_production_order(
    payload: ProductionOrderCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ManufacturingProductionOrder:
    tenant_id = _tenant_id(principal)
    exists = db.scalar(
        select(ManufacturingProductionOrder.id).where(
            ManufacturingProductionOrder.tenant_id == tenant_id,
            ManufacturingProductionOrder.order_number == payload.order_number,
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Production order number already exists")
    order = ManufacturingProductionOrder(
        tenant_id=tenant_id,
        **payload.model_dump(),
    )
    db.add(order)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Production order number already exists or facility is invalid",
        ) from exc
    db.refresh(order)
    return order


@router.get("/production-orders", response_model=list[ProductionOrderRead])
def list_production_orders(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ManufacturingProductionOrder]:
    tenant_id = _tenant_id(principal)
    return list(
        db.scalars(
            select(ManufacturingProductionOrder)
            .where(ManufacturingProductionOrder.tenant_id == tenant_id)
            .order_by(ManufacturingProductionOrder.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.post(
    "/metrics",
    response_model=MetricSampleRead,
    status_code=status.HTTP_201_CREATED,
)
def ingest_metric(
    payload: MetricSampleCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> ManufacturingMetricSample:
    sample = ManufacturingMetricSample(
        tenant_id=_tenant_id(principal),
        **payload.model_dump(),
    )
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


@router.get("/metrics", response_model=list[MetricSampleRead])
def list_metrics(
    equipment_code: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[ManufacturingMetricSample]:
    tenant_id = _tenant_id(principal)
    query = select(ManufacturingMetricSample).where(
        ManufacturingMetricSample.tenant_id == tenant_id
    )
    if equipment_code is not None:
        query = query.where(ManufacturingMetricSample.equipment_code == equipment_code)
    return list(
        db.scalars(
            query.order_by(ManufacturingMetricSample.observed_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )
