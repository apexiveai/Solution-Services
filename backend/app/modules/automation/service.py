import uuid
from datetime import datetime, time, timezone
from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.modules.automation.dependencies import record_audit
from app.modules.automation.models import (
    AutomationApproval,
    AutomationBot,
    AutomationExecution,
    AutomationQueueItem,
    AutomationTenantPolicy,
    AutomationWorkflow,
)
from app.modules.automation.runtime.engine import WorkflowExecutionError, execute_workflow
from app.modules.licensing.service import enforce_execution_entitlement, require_active_license
from app.security import CurrentPrincipal

ModelT = TypeVar("ModelT")
DEFAULT_POLICY = {
    "max_bots": 20,
    "max_concurrent_executions": 5,
    "max_executions_per_day": 1000,
}


def get_tenant_resource(
    db: Session,
    model: type[ModelT],
    resource_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> ModelT:
    resource = db.scalar(
        select(model).where(model.id == resource_id, model.tenant_id == tenant_id)
    )
    if resource is None:
        raise HTTPException(status_code=404, detail="Automation resource not found")
    return resource


def get_policy(db: Session, tenant_id: uuid.UUID) -> AutomationTenantPolicy | None:
    return db.scalar(
        select(AutomationTenantPolicy).where(AutomationTenantPolicy.tenant_id == tenant_id)
    )


def ensure_policy(
    db: Session,
    tenant_id: uuid.UUID,
    principal: CurrentPrincipal,
    *,
    lock: bool = False,
) -> AutomationTenantPolicy:
    db.execute(
        insert(AutomationTenantPolicy)
        .values(tenant_id=tenant_id, updated_by=principal.subject)
        .on_conflict_do_nothing(index_elements=["tenant_id"])
    )
    statement = select(AutomationTenantPolicy).where(
        AutomationTenantPolicy.tenant_id == tenant_id
    )
    if lock:
        statement = statement.with_for_update()
    policy = db.scalar(statement)
    if policy is None:
        raise RuntimeError("Unable to load automation tenant policy")
    return policy


def enforce_execution_limits(
    db: Session,
    tenant_id: uuid.UUID,
    principal: CurrentPrincipal,
    *,
    check_daily_limit: bool = True,
) -> AutomationTenantPolicy:
    policy = ensure_policy(db, tenant_id, principal, lock=True)
    running_count = db.scalar(
        select(func.count(AutomationExecution.id)).where(
            AutomationExecution.tenant_id == tenant_id,
            AutomationExecution.status == "RUNNING",
        )
    ) or 0
    if running_count >= policy.max_concurrent_executions:
        raise HTTPException(status_code=429, detail="Tenant concurrent execution limit reached")

    if check_daily_limit:
        start_of_day = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)
        executions_today = db.scalar(
            select(func.count(AutomationExecution.id)).where(
                AutomationExecution.tenant_id == tenant_id,
                AutomationExecution.created_at >= start_of_day,
            )
        ) or 0
        if executions_today >= policy.max_executions_per_day:
            raise HTTPException(status_code=429, detail="Tenant daily execution limit reached")
    return policy


def enqueue_workflow(
    db: Session,
    workflow: AutomationWorkflow,
    tenant_id: uuid.UUID,
    principal: CurrentPrincipal,
    input_data: dict,
    priority: int,
) -> AutomationExecution:
    if workflow.status != "PUBLISHED":
        raise HTTPException(status_code=409, detail="Only published workflows can be executed")

    enforce_execution_entitlement(db, tenant_id)
    enforce_execution_limits(db, tenant_id, principal)
    status_value = "PENDING_APPROVAL" if workflow.requires_approval else "QUEUED"
    execution = AutomationExecution(
        tenant_id=tenant_id,
        workflow_id=workflow.id,
        workflow_version=workflow.version,
        status=status_value,
        input_data=input_data,
        requested_by=principal.subject,
    )
    db.add(execution)
    db.flush()
    if workflow.requires_approval:
        db.add(
            AutomationApproval(
                tenant_id=tenant_id,
                execution_id=execution.id,
                requested_by=principal.subject,
            )
        )
    else:
        db.add(
            AutomationQueueItem(
                tenant_id=tenant_id,
                execution_id=execution.id,
                priority=priority,
            )
        )
    db.add(
        record_audit(
            tenant_id,
            principal,
            "execution.requested",
            "execution",
            execution.id,
            {"workflow_id": str(workflow.id), "requires_approval": workflow.requires_approval},
        )
    )
    return execution


def run_execution(
    db: Session,
    execution: AutomationExecution,
    workflow: AutomationWorkflow,
    principal: CurrentPrincipal,
    bot: AutomationBot | None = None,
) -> AutomationExecution:
    if execution.status != "QUEUED":
        raise HTTPException(status_code=409, detail="Execution is not queued")
    if workflow.definition.get("runtime", "CORE") != "CORE":
        raise HTTPException(
            status_code=409,
            detail="AIS and CY workflows must be executed by a registered studio runtime agent",
        )
    if workflow.status != "PUBLISHED":
        raise HTTPException(status_code=409, detail="Workflow is no longer published")
    require_active_license(db, execution.tenant_id)
    enforce_execution_limits(
        db,
        execution.tenant_id,
        principal,
        check_daily_limit=False,
    )
    if bot is None:
        raise HTTPException(status_code=409, detail="An idle registered bot is required")

    queue_item = db.scalar(
        select(AutomationQueueItem).where(
            AutomationQueueItem.tenant_id == execution.tenant_id,
            AutomationQueueItem.execution_id == execution.id,
            AutomationQueueItem.status == "READY",
        )
    )
    if queue_item is None:
        raise HTTPException(status_code=409, detail="Execution has no ready queue item")
    if bot is not None:
        if bot.status != "IDLE":
            raise HTTPException(status_code=409, detail="Bot must be idle before assignment")
        bot.status = "BUSY"
        bot.last_heartbeat_at = datetime.now(timezone.utc)
        execution.bot_id = bot.id

    execution.status = "RUNNING"
    execution.started_at = datetime.now(timezone.utc)
    queue_item.status = "CLAIMED"
    queue_item.attempts += 1
    db.flush()
    try:
        execution.result_data = execute_workflow(workflow.definition, execution.input_data)
        execution.status = "SUCCEEDED"
        queue_item.status = "DONE"
    except (WorkflowExecutionError, ValueError) as exc:
        execution.status = "FAILED"
        execution.error_message = str(exc)[:2000]
        queue_item.status = "DEAD"
    finally:
        execution.finished_at = datetime.now(timezone.utc)
        if bot is not None:
            bot.status = "IDLE"
    db.add(
        record_audit(
            execution.tenant_id,
            principal,
            "execution.completed" if execution.status == "SUCCEEDED" else "execution.failed",
            "execution",
            execution.id,
            {"status": execution.status, "workflow_version": execution.workflow_version},
        )
    )
    db.commit()
    db.refresh(execution)
    return execution
