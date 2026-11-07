import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.dependencies import record_audit, require_automation_role, tenant_uuid
from app.modules.automation.models import (
    AutomationBot,
    AutomationExecution,
    AutomationQueueItem,
    AutomationWorkflow,
)
from app.modules.automation.schemas import ExecutionRead, RunCreate, RunExecution
from app.modules.automation.service import enqueue_workflow, get_tenant_resource, run_execution
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(tags=["Automation Executions"])


@router.post(
    "/workflows/{workflow_id}/executions",
    response_model=ExecutionRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def request_execution(
    workflow_id: uuid.UUID,
    payload: RunCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationExecution:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    workflow = get_tenant_resource(db, AutomationWorkflow, workflow_id, tenant_id)
    execution = enqueue_workflow(
        db,
        workflow,
        tenant_id,
        principal,
        payload.input_data,
        payload.priority,
    )
    db.commit()
    db.refresh(execution)
    return execution


@router.get("/executions")
def list_executions(
    execution_status: str | None = Query(default=None, alias="status", max_length=24),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationExecution).where(AutomationExecution.tenant_id == tenant_id)
    if execution_status:
        statement = statement.where(AutomationExecution.status == execution_status.upper())
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationExecution.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [ExecutionRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/executions/{execution_id}/run", response_model=ExecutionRead)
def start_execution(
    execution_id: uuid.UUID,
    payload: RunExecution = RunExecution(),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationExecution:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    execution = get_tenant_resource(db, AutomationExecution, execution_id, tenant_id)
    workflow = get_tenant_resource(db, AutomationWorkflow, execution.workflow_id, tenant_id)
    bot = (
        get_tenant_resource(db, AutomationBot, payload.bot_id, tenant_id)
        if payload.bot_id
        else None
    )
    return run_execution(db, execution, workflow, principal, bot)


@router.post("/executions/{execution_id}/cancel", response_model=ExecutionRead)
def cancel_execution(
    execution_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationExecution:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    execution = get_tenant_resource(db, AutomationExecution, execution_id, tenant_id)
    if execution.status not in {"QUEUED", "PENDING_APPROVAL"}:
        raise HTTPException(status_code=409, detail="Only queued or approval-pending executions can be cancelled")
    execution.status = "CANCELLED"
    queue_item = db.scalar(
        select(AutomationQueueItem).where(
            AutomationQueueItem.tenant_id == tenant_id,
            AutomationQueueItem.execution_id == execution.id,
            AutomationQueueItem.status == "READY",
        )
    )
    if queue_item:
        queue_item.status = "DEAD"
    db.add(record_audit(tenant_id, principal, "execution.cancelled", "execution", execution.id))
    db.commit()
    db.refresh(execution)
    return execution


@router.post(
    "/executions/{execution_id}/retry",
    response_model=ExecutionRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def retry_execution(
    execution_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationExecution:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    failed_execution = get_tenant_resource(db, AutomationExecution, execution_id, tenant_id)
    if failed_execution.status != "FAILED":
        raise HTTPException(status_code=409, detail="Only failed executions can be retried")
    workflow = get_tenant_resource(
        db, AutomationWorkflow, failed_execution.workflow_id, tenant_id
    )
    retry = enqueue_workflow(
        db,
        workflow,
        tenant_id,
        principal,
        failed_execution.input_data,
        priority=5,
    )
    db.add(record_audit(tenant_id, principal, "execution.retry_requested", "execution", failed_execution.id))
    db.commit()
    db.refresh(retry)
    return retry
