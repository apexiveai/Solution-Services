import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.dependencies import record_audit, require_automation_role, tenant_uuid
from app.modules.automation.models import (
    AutomationBot,
    AutomationExecution,
    AutomationQueueItem,
    AutomationWorkflow,
)
from app.modules.automation.schemas import (
    BotControl,
    BotCreate,
    BotRead,
    RuntimeClaimRead,
    RuntimeCompletionCreate,
)
from app.modules.automation.service import ensure_policy, get_tenant_resource
from app.modules.licensing.service import (
    enforce_bot_entitlement,
    require_active_license,
    require_developer_seat,
)
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/bots", tags=["Automation Bots"])


@router.get("")
def list_bots(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationBot).where(AutomationBot.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(statement.order_by(AutomationBot.created_at.desc()).offset(offset).limit(limit))
    )
    return {
        "items": [BotRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", response_model=BotRead, status_code=status.HTTP_201_CREATED)
def register_bot(
    payload: BotCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationBot:
    require_automation_role(principal, "admin", "developer", "agent")
    if "core_rpa_agent" in {role.casefold() for role in principal.roles} and (
        not payload.capabilities
        or not set(payload.capabilities).issubset({"runtime:AIS", "runtime:CY"})
    ):
        raise HTTPException(
            status_code=422,
            detail="Agent identities may register only AIS or CY runtime capabilities",
        )
    tenant_id = tenant_uuid(principal)
    require_developer_seat(db, tenant_id, principal.subject, principal.roles)
    enforce_bot_entitlement(db, tenant_id)
    policy = ensure_policy(db, tenant_id, principal, lock=True)
    bot_count = db.scalar(
        select(func.count(AutomationBot.id)).where(AutomationBot.tenant_id == tenant_id)
    ) or 0
    if bot_count >= policy.max_bots:
        db.rollback()
        raise HTTPException(status_code=429, detail="Tenant bot limit reached")

    bot = AutomationBot(
        tenant_id=tenant_id,
        name=payload.name.strip(),
        capabilities=payload.capabilities,
        worker_version=payload.worker_version,
        registered_by=principal.subject,
    )
    db.add(bot)
    try:
        db.flush()
        db.add(record_audit(tenant_id, principal, "bot.registered", "bot", bot.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A bot with this name already exists") from exc
    db.refresh(bot)
    return bot


@router.post("/{bot_id}/control", response_model=BotRead)
def control_bot(
    bot_id: uuid.UUID,
    payload: BotControl,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationBot:
    roles = {role.casefold() for role in principal.roles}
    require_automation_role(principal, "admin", "operator", "agent")
    tenant_id = tenant_uuid(principal)
    bot = get_tenant_resource(db, AutomationBot, bot_id, tenant_id)
    if "core_rpa_agent" in roles and (
        bot.registered_by != principal.subject or payload.action not in {"START", "STOP"}
    ):
        raise HTTPException(status_code=403, detail="Agent identities may only start or stop their own bot")
    valid_transitions = {
        ("OFFLINE", "START"): "IDLE",
        ("IDLE", "STOP"): "OFFLINE",
        ("PAUSED", "STOP"): "OFFLINE",
        ("IDLE", "PAUSE"): "PAUSED",
        ("PAUSED", "RESUME"): "IDLE",
    }
    next_status = valid_transitions.get((bot.status, payload.action))
    if next_status is None:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot {payload.action.lower()} a bot in {bot.status.lower()} state",
        )
    bot.status = next_status
    bot.last_heartbeat_at = datetime.now(timezone.utc) if next_status == "IDLE" else bot.last_heartbeat_at
    db.add(record_audit(tenant_id, principal, f"bot.{payload.action.lower()}", "bot", bot.id))
    db.commit()
    db.refresh(bot)
    return bot


@router.post("/{bot_id}/heartbeat", response_model=BotRead)
def heartbeat_bot(
    bot_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationBot:
    require_automation_role(principal, "admin", "operator", "agent")
    bot = get_tenant_resource(db, AutomationBot, bot_id, tenant_uuid(principal))
    if (
        "core_rpa_agent" in {role.casefold() for role in principal.roles}
        and bot.registered_by != principal.subject
    ):
        raise HTTPException(status_code=403, detail="This bot belongs to another agent identity")
    if bot.status == "OFFLINE":
        raise HTTPException(status_code=409, detail="An offline bot cannot send a heartbeat")
    bot.last_heartbeat_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bot)
    return bot


@router.post("/{bot_id}/claim", response_model=RuntimeClaimRead | None)
def claim_studio_execution(
    bot_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> RuntimeClaimRead | None:
    require_automation_role(principal, "agent")
    tenant_id = tenant_uuid(principal)
    bot = db.scalar(
        select(AutomationBot)
        .where(AutomationBot.id == bot_id, AutomationBot.tenant_id == tenant_id)
        .with_for_update()
    )
    if bot is None:
        raise HTTPException(status_code=404, detail="Automation bot not found")
    if bot.registered_by != principal.subject:
        raise HTTPException(status_code=403, detail="This bot belongs to another agent identity")
    now = datetime.now(timezone.utc)
    if (
        bot.status == "BUSY"
        and (
            bot.last_heartbeat_at is None
            or bot.last_heartbeat_at < now - timedelta(minutes=2)
        )
    ):
        stale_execution = db.scalar(
            select(AutomationExecution)
            .where(
                AutomationExecution.tenant_id == tenant_id,
                AutomationExecution.bot_id == bot.id,
                AutomationExecution.status == "RUNNING",
            )
            .with_for_update()
        )
        if stale_execution is not None:
            stale_queue_item = db.scalar(
                select(AutomationQueueItem)
                .where(
                    AutomationQueueItem.tenant_id == tenant_id,
                    AutomationQueueItem.execution_id == stale_execution.id,
                    AutomationQueueItem.status == "CLAIMED",
                )
                .with_for_update()
            )
            if stale_queue_item is not None:
                stale_queue_item.status = "READY"
                stale_execution.status = "QUEUED"
                stale_execution.bot_id = None
                stale_execution.started_at = None
                db.add(
                    record_audit(
                        tenant_id,
                        principal,
                        "studio_execution.requeued",
                        "execution",
                        stale_execution.id,
                        {"reason": "agent heartbeat expired"},
                    )
                )
            else:
                stale_execution.status = "FAILED"
                stale_execution.error_message = "The agent lease expired without a claimed queue item."
                stale_execution.finished_at = now
        bot.status = "IDLE"
    if bot.status != "IDLE":
        raise HTTPException(status_code=409, detail="The agent bot must be idle to claim work")

    capabilities = set(bot.capabilities)
    if not capabilities.intersection({"runtime:AIS", "runtime:CY"}):
        raise HTTPException(status_code=403, detail="The bot has no AIS or CY runtime capability")
    require_active_license(db, tenant_id)

    candidates = db.scalars(
        select(AutomationQueueItem)
        .join(
            AutomationExecution,
            (AutomationExecution.id == AutomationQueueItem.execution_id)
            & (AutomationExecution.tenant_id == AutomationQueueItem.tenant_id),
        )
        .join(
            AutomationWorkflow,
            (AutomationWorkflow.id == AutomationExecution.workflow_id)
            & (AutomationWorkflow.tenant_id == AutomationExecution.tenant_id),
        )
        .where(
            AutomationQueueItem.tenant_id == tenant_id,
            AutomationQueueItem.status == "READY",
            AutomationQueueItem.available_at <= now,
            AutomationExecution.status == "QUEUED",
            AutomationWorkflow.definition["runtime"].as_string().in_(
                [
                    runtime
                    for runtime in ("AIS", "CY")
                    if f"runtime:{runtime}" in capabilities
                ]
            ),
        )
        .order_by(AutomationQueueItem.priority.asc(), AutomationQueueItem.created_at.asc())
        .with_for_update(skip_locked=True, of=AutomationQueueItem)
        .limit(100)
    )
    for queue_item in candidates:
        execution = db.scalar(
            select(AutomationExecution)
            .where(
                AutomationExecution.id == queue_item.execution_id,
                AutomationExecution.tenant_id == tenant_id,
            )
            .with_for_update()
        )
        if execution is None or execution.status != "QUEUED":
            queue_item.status = "DEAD"
            continue
        workflow = db.scalar(
            select(AutomationWorkflow).where(
                AutomationWorkflow.id == execution.workflow_id,
                AutomationWorkflow.tenant_id == tenant_id,
            )
        )
        if workflow is None or workflow.status != "PUBLISHED":
            queue_item.status = "DEAD"
            execution.status = "FAILED"
            execution.error_message = "Workflow definition is unavailable or unpublished."
            execution.finished_at = datetime.now(timezone.utc)
            continue

        runtime = workflow.definition.get("runtime", "CORE")
        if runtime not in {"AIS", "CY"} or f"runtime:{runtime}" not in capabilities:
            continue

        bot.status = "BUSY"
        bot.last_heartbeat_at = now
        execution.status = "RUNNING"
        execution.bot_id = bot.id
        execution.started_at = now
        queue_item.status = "CLAIMED"
        queue_item.attempts += 1
        db.add(
            record_audit(
                tenant_id,
                principal,
                "studio_execution.claimed",
                "execution",
                execution.id,
                {"runtime": runtime, "workflow_version": execution.workflow_version},
            )
        )
        response = RuntimeClaimRead(
            execution_id=execution.id,
            tenant_id=tenant_id,
            workflow_id=workflow.id,
            workflow_version=execution.workflow_version,
            claim_attempt=queue_item.attempts,
            contract_version=1,
            runtime=runtime,
            definition=workflow.definition,
            input_data=execution.input_data,
        )
        db.commit()
        return response

    db.commit()
    return None


@router.post("/{bot_id}/executions/{execution_id}/complete", status_code=204)
def complete_studio_execution(
    bot_id: uuid.UUID,
    execution_id: uuid.UUID,
    payload: RuntimeCompletionCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> None:
    require_automation_role(principal, "agent")
    tenant_id = tenant_uuid(principal)
    bot = get_tenant_resource(db, AutomationBot, bot_id, tenant_id)
    if bot.registered_by != principal.subject:
        raise HTTPException(status_code=403, detail="This bot belongs to another agent identity")

    execution = db.scalar(
        select(AutomationExecution)
        .where(
            AutomationExecution.id == execution_id,
            AutomationExecution.tenant_id == tenant_id,
            AutomationExecution.bot_id == bot.id,
            AutomationExecution.status == "RUNNING",
        )
        .with_for_update()
    )
    if execution is None:
        raise HTTPException(status_code=409, detail="No running execution is assigned to this bot")
    queue_item = db.scalar(
        select(AutomationQueueItem).where(
            AutomationQueueItem.execution_id == execution.id,
            AutomationQueueItem.tenant_id == tenant_id,
            AutomationQueueItem.status == "CLAIMED",
        )
    )
    if queue_item is None:
        raise HTTPException(status_code=409, detail="The execution has no claimed queue item")
    if queue_item.attempts != payload.claim_attempt:
        raise HTTPException(status_code=409, detail="This execution claim has expired")

    workflow = get_tenant_resource(db, AutomationWorkflow, execution.workflow_id, tenant_id)
    runtime = workflow.definition.get("runtime", "CORE")
    if runtime not in {"AIS", "CY"} or f"runtime:{runtime}" not in set(bot.capabilities):
        raise HTTPException(status_code=409, detail="The assigned workflow runtime does not match the agent")

    now = datetime.now(timezone.utc)
    execution.status = payload.status
    execution.result_data = payload.result_data if payload.status == "SUCCEEDED" else None
    execution.error_message = payload.error_message if payload.status == "FAILED" else None
    execution.finished_at = now
    queue_item.status = "DONE" if payload.status == "SUCCEEDED" else "DEAD"
    bot.status = "IDLE"
    bot.last_heartbeat_at = now
    db.add(
        record_audit(
            tenant_id,
            principal,
            "studio_execution.completed"
            if payload.status == "SUCCEEDED"
            else "studio_execution.failed",
            "execution",
            execution.id,
            {"runtime": runtime, "workflow_version": execution.workflow_version},
        )
    )
    db.commit()
