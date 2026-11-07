from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.dependencies import tenant_uuid
from app.modules.automation.models import AutomationExecution
from app.modules.automation.monitoring.service import tenant_monitoring
from app.modules.automation.schemas import BotRead, ExecutionRead
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(tags=["Automation Monitoring"])


@router.get("/monitoring")
def get_monitoring(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    data = tenant_monitoring(db, tenant_uuid(principal))
    return {
        "bots": [BotRead.model_validate(bot).model_dump(mode="json") for bot in data["bots"]],
        "running_executions": [
            ExecutionRead.model_validate(execution).model_dump(mode="json")
            for execution in data["running_executions"]
        ],
        "queued_executions": data["queued_executions"],
    }


@router.get("/exceptions")
def list_exceptions(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationExecution).where(
        AutomationExecution.tenant_id == tenant_id,
        AutomationExecution.status == "FAILED",
    )
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationExecution.finished_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )
    return {
        "items": [ExecutionRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
