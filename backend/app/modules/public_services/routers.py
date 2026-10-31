import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.public_services.catalog import SOLUTION_CATALOG
from app.modules.public_services.models import PublicEmergencyIncident, PublicServiceCase
from app.modules.public_services.schemas import (
    EmergencyIncidentCreate,
    EmergencyIncidentRead,
    ServiceCaseCreate,
    ServiceCaseRead,
)
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/public-services", tags=["Public Services"])


def _tenant_id(principal: CurrentPrincipal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token contains an invalid tenant_id claim",
        ) from exc


@router.get("/catalog")
def get_solution_catalog(
    _: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    return {"solutions": SOLUTION_CATALOG}


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = _tenant_id(principal)
    case_counts = db.execute(
        select(PublicServiceCase.status, func.count(PublicServiceCase.id))
        .where(PublicServiceCase.tenant_id == tenant_id)
        .group_by(PublicServiceCase.status)
    ).all()
    incident_counts = db.execute(
        select(PublicEmergencyIncident.status, func.count(PublicEmergencyIncident.id))
        .where(PublicEmergencyIncident.tenant_id == tenant_id)
        .group_by(PublicEmergencyIncident.status)
    ).all()
    return {
        "solutions": len(SOLUTION_CATALOG),
        "service_cases_by_status": dict(case_counts),
        "emergency_incidents_by_status": dict(incident_counts),
    }


@router.post(
    "/cases",
    response_model=ServiceCaseRead,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    payload: ServiceCaseCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> PublicServiceCase:
    tenant_id = _tenant_id(principal)
    exists = db.scalar(
        select(PublicServiceCase.id).where(
            PublicServiceCase.tenant_id == tenant_id,
            PublicServiceCase.case_number == payload.case_number,
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Case number already exists")
    case = PublicServiceCase(tenant_id=tenant_id, **payload.model_dump())
    db.add(case)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Case number already exists") from exc
    db.refresh(case)
    return case


@router.get("/cases", response_model=list[ServiceCaseRead])
def list_cases(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[PublicServiceCase]:
    tenant_id = _tenant_id(principal)
    return list(
        db.scalars(
            select(PublicServiceCase)
            .where(PublicServiceCase.tenant_id == tenant_id)
            .order_by(PublicServiceCase.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.post(
    "/incidents",
    response_model=EmergencyIncidentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    payload: EmergencyIncidentCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> PublicEmergencyIncident:
    tenant_id = _tenant_id(principal)
    exists = db.scalar(
        select(PublicEmergencyIncident.id).where(
            PublicEmergencyIncident.tenant_id == tenant_id,
            PublicEmergencyIncident.incident_number == payload.incident_number,
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Incident number already exists")
    incident = PublicEmergencyIncident(tenant_id=tenant_id, **payload.model_dump())
    db.add(incident)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Incident number already exists") from exc
    db.refresh(incident)
    return incident


@router.get("/incidents", response_model=list[EmergencyIncidentRead])
def list_incidents(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[PublicEmergencyIncident]:
    tenant_id = _tenant_id(principal)
    return list(
        db.scalars(
            select(PublicEmergencyIncident)
            .where(PublicEmergencyIncident.tenant_id == tenant_id)
            .order_by(PublicEmergencyIncident.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )
