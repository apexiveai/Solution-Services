import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditEvent
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])


@router.get("/recent")
def recent_audit_events(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[dict]:
    try:
        tenant_id = uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="Invalid tenant claim") from exc
    events = db.scalars(
        select(AuditEvent)
        .where(AuditEvent.tenant_id == tenant_id)
        .order_by(AuditEvent.created_at.desc())
        .limit(limit)
    )
    return [
        {
            "id": str(event.id),
            "actor_subject": event.actor_subject,
            "action": event.action,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "details": event.details,
            "success": event.success,
            "created_at": event.created_at,
        }
        for event in events
    ]
