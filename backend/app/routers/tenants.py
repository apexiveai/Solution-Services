import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tenant
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/tenants", tags=["Tenants"])


@router.get("/current")
def current_tenant(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    try:
        tenant_id = uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="Token contains an invalid tenant_id claim") from exc

    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {
        "id": str(tenant.id),
        "code": tenant.code,
        "name": tenant.name,
        "status": tenant.status,
        "created_at": tenant.created_at,
    }
