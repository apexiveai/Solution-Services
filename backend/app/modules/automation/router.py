import uuid
from datetime import datetime, time, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.analytics.service import execution_analytics
from app.modules.automation.bots.router import router as bots_router
from app.modules.automation.crypto import encrypt_secret
from app.modules.automation.dependencies import (
    record_audit,
    require_automation_role,
    tenant_uuid,
)
from app.modules.automation.designer.router import router as designer_router
from app.modules.automation.executions.router import router as executions_router
from app.modules.automation.models import (
    AutomationApproval,
    AutomationAuditEvent,
    AutomationBot,
    AutomationCredential,
    AutomationExecution,
    AutomationIntegration,
    AutomationQueueItem,
    AutomationSchedule,
    AutomationTenantPolicy,
    AutomationTemplate,
    AutomationTrigger,
    AutomationWorkflow,
    AutomationWorkflowVersion,
)
from app.modules.automation.monitoring.router import router as monitoring_router
from app.modules.automation.schemas import (
    ApprovalDecision,
    ApprovalRead,
    CredentialCreate,
    CredentialRead,
    EnabledUpdate,
    ExecutionRead,
    IntegrationCreate,
    IntegrationRead,
    QueueRead,
    ScheduleCreate,
    ScheduleRead,
    TenantPolicyRead,
    TenantPolicyUpdate,
    TemplateCreate,
    TemplateRead,
    TriggerCreate,
    TriggerFire,
    TriggerRead,
    WorkflowRead,
)
from app.modules.automation.scheduler.service import next_schedule_run
from app.modules.automation.service import (
    DEFAULT_POLICY,
    enqueue_workflow,
    ensure_policy,
    get_policy,
    get_tenant_resource,
)
from app.modules.automation.triggers.service import get_enabled_trigger
from app.modules.automation.workflows.router import router as workflows_router
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/automation", tags=["Apexive CoreRPA"])
router.include_router(designer_router)
router.include_router(workflows_router)
router.include_router(bots_router)
router.include_router(executions_router)
router.include_router(monitoring_router)


def _count(db: Session, model: type, *conditions) -> int:
    return db.scalar(select(func.count(model.id)).where(*conditions)) or 0


def _policy_values(policy: AutomationTenantPolicy | None, tenant_id: uuid.UUID) -> dict:
    if policy is None:
        return {"tenant_id": tenant_id, **DEFAULT_POLICY}
    return {
        "tenant_id": policy.tenant_id,
        "max_bots": policy.max_bots,
        "max_concurrent_executions": policy.max_concurrent_executions,
        "max_executions_per_day": policy.max_executions_per_day,
        "updated_by": policy.updated_by,
        "updated_at": policy.updated_at,
    }


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    start_of_day = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)
    executions_today = _count(
        db,
        AutomationExecution,
        AutomationExecution.tenant_id == tenant_id,
        AutomationExecution.created_at >= start_of_day,
    )
    executions = execution_analytics(db, tenant_id)
    return {
        "workflows": _count(db, AutomationWorkflow, AutomationWorkflow.tenant_id == tenant_id),
        "active_bots": _count(
            db,
            AutomationBot,
            AutomationBot.tenant_id == tenant_id,
            AutomationBot.status.in_(("IDLE", "BUSY")),
        ),
        "queued_executions": _count(
            db,
            AutomationQueueItem,
            AutomationQueueItem.tenant_id == tenant_id,
            AutomationQueueItem.status == "READY",
        ),
        "pending_approvals": _count(
            db,
            AutomationApproval,
            AutomationApproval.tenant_id == tenant_id,
            AutomationApproval.status == "PENDING",
        ),
        "executions_today": executions_today,
        "failure_rate": executions["failure_rate"],
    }


@router.get("/queues")
def list_queue(
    queue_status: str | None = Query(default=None, alias="status", max_length=24),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationQueueItem).where(AutomationQueueItem.tenant_id == tenant_id)
    if queue_status:
        statement = statement.where(AutomationQueueItem.status == queue_status.upper())
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(
                AutomationQueueItem.priority.asc(),
                AutomationQueueItem.created_at.asc(),
            )
            .offset(offset)
            .limit(limit)
        )
    )
    return {
        "items": [QueueRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/queues/{queue_id}/retry", response_model=ExecutionRead, status_code=202)
def retry_queue_item(
    queue_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    item = get_tenant_resource(db, AutomationQueueItem, queue_id, tenant_id)
    if item.status != "DEAD":
        raise HTTPException(status_code=409, detail="Only a dead queue item can be retried")
    failed_execution = get_tenant_resource(
        db, AutomationExecution, item.execution_id, tenant_id
    )
    workflow = get_tenant_resource(
        db, AutomationWorkflow, failed_execution.workflow_id, tenant_id
    )
    new_execution = enqueue_workflow(
        db,
        workflow,
        tenant_id,
        principal,
        failed_execution.input_data,
        item.priority,
    )
    db.add(record_audit(tenant_id, principal, "queue.retry_requested", "queue", item.id))
    db.commit()
    db.refresh(new_execution)
    return new_execution


@router.get("/schedules")
def list_schedules(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationSchedule).where(AutomationSchedule.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationSchedule.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [ScheduleRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/schedules", response_model=ScheduleRead, status_code=201)
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationSchedule:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    workflow = get_tenant_resource(db, AutomationWorkflow, payload.workflow_id, tenant_id)
    if workflow.status != "PUBLISHED":
        raise HTTPException(status_code=409, detail="Schedules require a published workflow")
    schedule = AutomationSchedule(
        tenant_id=tenant_id,
        workflow_id=workflow.id,
        name=payload.name.strip(),
        cron_expression=payload.cron_expression,
        timezone_name=payload.timezone_name,
        enabled=payload.enabled,
        next_run_at=(
            next_schedule_run(payload.cron_expression, payload.timezone_name)
            if payload.enabled
            else None
        ),
        created_by=principal.subject,
    )
    db.add(schedule)
    db.add(record_audit(tenant_id, principal, "schedule.created", "schedule"))
    db.commit()
    db.refresh(schedule)
    return schedule


@router.post("/schedules/{schedule_id}/toggle", response_model=ScheduleRead)
def toggle_schedule(
    schedule_id: uuid.UUID,
    enabled: bool = Query(...),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationSchedule:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    schedule = get_tenant_resource(db, AutomationSchedule, schedule_id, tenant_id)
    schedule.enabled = enabled
    schedule.next_run_at = (
        next_schedule_run(schedule.cron_expression, schedule.timezone_name)
        if enabled
        else None
    )
    db.add(record_audit(tenant_id, principal, "schedule.toggled", "schedule", schedule.id))
    db.commit()
    db.refresh(schedule)
    return schedule


@router.post("/schedules/{schedule_id}/run", response_model=ExecutionRead, status_code=202)
def run_schedule_now(
    schedule_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    schedule = get_tenant_resource(db, AutomationSchedule, schedule_id, tenant_id)
    workflow = get_tenant_resource(db, AutomationWorkflow, schedule.workflow_id, tenant_id)
    execution = enqueue_workflow(db, workflow, tenant_id, principal, {}, priority=5)
    db.add(record_audit(tenant_id, principal, "schedule.run_requested", "schedule", schedule.id))
    db.commit()
    db.refresh(execution)
    return execution


@router.get("/triggers")
def list_triggers(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationTrigger).where(AutomationTrigger.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationTrigger.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [TriggerRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/triggers", response_model=TriggerRead, status_code=201)
def create_trigger(
    payload: TriggerCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationTrigger:
    require_automation_role(principal, "admin", "developer")
    tenant_id = tenant_uuid(principal)
    workflow = get_tenant_resource(db, AutomationWorkflow, payload.workflow_id, tenant_id)
    if workflow.status != "PUBLISHED":
        raise HTTPException(status_code=409, detail="Triggers require a published workflow")
    trigger = AutomationTrigger(
        tenant_id=tenant_id,
        workflow_id=workflow.id,
        name=payload.name.strip(),
        event_name=payload.event_name.strip(),
        enabled=payload.enabled,
        created_by=principal.subject,
    )
    db.add(trigger)
    db.add(record_audit(tenant_id, principal, "trigger.created", "trigger"))
    db.commit()
    db.refresh(trigger)
    return trigger


@router.post("/triggers/{trigger_id}/fire", response_model=ExecutionRead, status_code=202)
def fire_trigger(
    trigger_id: uuid.UUID,
    payload: TriggerFire,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    trigger = get_enabled_trigger(db, tenant_id, trigger_id)
    if trigger is None:
        raise HTTPException(status_code=404, detail="Enabled trigger not found")
    workflow = get_tenant_resource(db, AutomationWorkflow, trigger.workflow_id, tenant_id)
    execution = enqueue_workflow(db, workflow, tenant_id, principal, payload.input_data, priority=5)
    db.add(record_audit(tenant_id, principal, "trigger.fired", "trigger", trigger.id))
    db.commit()
    db.refresh(execution)
    return execution


@router.patch("/triggers/{trigger_id}", response_model=TriggerRead)
def update_trigger(
    trigger_id: uuid.UUID,
    payload: EnabledUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationTrigger:
    require_automation_role(principal, "admin", "developer")
    tenant_id = tenant_uuid(principal)
    trigger = get_tenant_resource(db, AutomationTrigger, trigger_id, tenant_id)
    trigger.enabled = payload.enabled
    db.add(record_audit(tenant_id, principal, "trigger.toggled", "trigger", trigger.id))
    db.commit()
    db.refresh(trigger)
    return trigger


@router.get("/approvals")
def list_approvals(
    approval_status: str | None = Query(default=None, alias="status", max_length=24),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationApproval).where(AutomationApproval.tenant_id == tenant_id)
    if approval_status:
        statement = statement.where(AutomationApproval.status == approval_status.upper())
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationApproval.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [ApprovalRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/approvals/{approval_id}/decision", response_model=ApprovalRead)
def decide_approval(
    approval_id: uuid.UUID,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationApproval:
    require_automation_role(principal, "admin", "operator")
    tenant_id = tenant_uuid(principal)
    approval = get_tenant_resource(db, AutomationApproval, approval_id, tenant_id)
    if approval.status != "PENDING":
        raise HTTPException(status_code=409, detail="Approval has already been reviewed")
    if approval.requested_by == principal.subject:
        raise HTTPException(status_code=403, detail="The requester cannot approve their own execution")
    execution = get_tenant_resource(db, AutomationExecution, approval.execution_id, tenant_id)
    if execution.status != "PENDING_APPROVAL":
        raise HTTPException(status_code=409, detail="Execution is no longer awaiting approval")

    approval.status = payload.decision
    approval.reviewed_by = principal.subject
    approval.review_note = payload.note
    approval.reviewed_at = datetime.now(timezone.utc)
    if payload.decision == "APPROVED":
        execution.status = "QUEUED"
        db.add(AutomationQueueItem(tenant_id=tenant_id, execution_id=execution.id))
    else:
        execution.status = "FAILED"
        execution.error_message = "Execution rejected by an approver"
        execution.finished_at = datetime.now(timezone.utc)
    db.add(
        record_audit(
            tenant_id,
            principal,
            f"approval.{payload.decision.lower()}",
            "approval",
            approval.id,
            {"execution_id": str(execution.id)},
        )
    )
    db.commit()
    db.refresh(approval)
    return approval


@router.get("/integrations")
def list_integrations(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationIntegration).where(AutomationIntegration.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationIntegration.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [IntegrationRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/integrations", response_model=IntegrationRead, status_code=201)
def create_integration(
    payload: IntegrationCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationIntegration:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    if payload.credential_id:
        credential = db.scalar(
            select(AutomationCredential).where(
                AutomationCredential.id == payload.credential_id,
                AutomationCredential.tenant_id == tenant_id,
            )
        )
        if credential is None:
            raise HTTPException(status_code=404, detail="Tenant credential not found")
    integration = AutomationIntegration(
        tenant_id=tenant_id,
        name=payload.name.strip(),
        connector_type=payload.connector_type,
        approved_hosts=payload.approved_hosts,
        credential_id=payload.credential_id,
        created_by=principal.subject,
    )
    db.add(integration)
    try:
        db.flush()
        db.add(record_audit(tenant_id, principal, "integration.registered", "integration", integration.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="An integration with this name already exists") from exc
    db.refresh(integration)
    return integration


@router.post("/integrations/{integration_id}/enable", response_model=IntegrationRead)
def enable_integration(
    integration_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationIntegration:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    integration = get_tenant_resource(db, AutomationIntegration, integration_id, tenant_id)
    if not integration.approved_hosts:
        raise HTTPException(status_code=409, detail="An explicit approved host allowlist is required")
    integration.enabled = True
    db.add(record_audit(tenant_id, principal, "integration.enabled", "integration", integration.id))
    db.commit()
    db.refresh(integration)
    return integration


@router.post("/integrations/{integration_id}/disable", response_model=IntegrationRead)
def disable_integration(
    integration_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationIntegration:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    integration = get_tenant_resource(db, AutomationIntegration, integration_id, tenant_id)
    integration.enabled = False
    db.add(record_audit(tenant_id, principal, "integration.disabled", "integration", integration.id))
    db.commit()
    db.refresh(integration)
    return integration


@router.get("/templates")
def list_templates(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationTemplate).where(AutomationTemplate.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationTemplate.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [TemplateRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/templates", response_model=TemplateRead, status_code=201)
def create_template(
    payload: TemplateCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationTemplate:
    require_automation_role(principal, "admin", "developer")
    tenant_id = tenant_uuid(principal)
    template = AutomationTemplate(
        tenant_id=tenant_id,
        name=payload.name.strip(),
        description=payload.description,
        category=payload.category,
        definition=payload.definition,
        created_by=principal.subject,
    )
    db.add(template)
    db.add(record_audit(tenant_id, principal, "template.created", "template"))
    db.commit()
    db.refresh(template)
    return template


@router.post(
    "/templates/{template_id}/instantiate",
    response_model=WorkflowRead,
    status_code=201,
)
def instantiate_template(
    template_id: uuid.UUID,
    name: str = Query(min_length=1, max_length=160),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationWorkflow:
    require_automation_role(principal, "admin", "developer")
    tenant_id = tenant_uuid(principal)
    template = get_tenant_resource(db, AutomationTemplate, template_id, tenant_id)
    workflow = AutomationWorkflow(
        tenant_id=tenant_id,
        name=name.strip(),
        description=template.description,
        definition=template.definition,
        created_by=principal.subject,
    )
    db.add(workflow)
    try:
        db.flush()
        db.add(
            AutomationWorkflowVersion(
                tenant_id=tenant_id,
                workflow_id=workflow.id,
                version=workflow.version,
                definition=workflow.definition,
                actor_subject=principal.subject,
            )
        )
        db.add(record_audit(tenant_id, principal, "template.instantiated", "template", template.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A workflow with this name already exists") from exc
    db.refresh(workflow)
    return workflow


@router.get("/credentials")
def list_credentials(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationCredential).where(AutomationCredential.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    credentials = list(
        db.scalars(
            statement.order_by(AutomationCredential.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [
            CredentialRead.model_validate(item).model_dump(mode="json")
            for item in credentials
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("/credentials", response_model=CredentialRead, status_code=201)
def create_credential(
    payload: CredentialCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationCredential:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    try:
        encrypted = encrypt_secret(payload.secret.get_secret_value())
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    credential = AutomationCredential(
        tenant_id=tenant_id,
        name=payload.name.strip(),
        encrypted_secret=encrypted,
        created_by=principal.subject,
    )
    db.add(credential)
    try:
        db.flush()
        db.add(record_audit(tenant_id, principal, "credential.created", "credential", credential.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A credential with this name already exists") from exc
    db.refresh(credential)
    return credential


@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    return execution_analytics(db, tenant_uuid(principal))


@router.get("/governance")
@router.get("/settings")
def get_governance(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    policy = get_policy(db, tenant_id)
    audit_items = list(
        db.scalars(
            select(AutomationAuditEvent)
            .where(AutomationAuditEvent.tenant_id == tenant_id)
            .order_by(AutomationAuditEvent.created_at.desc())
            .limit(20)
        )
    )
    return {
        "policy": _policy_values(policy, tenant_id),
        "credentials": _count(
            db, AutomationCredential, AutomationCredential.tenant_id == tenant_id
        ),
        "roles": [
            {"role": "admin", "permissions": ["governance", "credentials", "all operations"]},
            {"role": "developer", "permissions": ["workflow design", "templates", "triggers"]},
            {"role": "operator", "permissions": ["execution", "bots", "approvals"]},
            {"role": "viewer", "permissions": ["read-only access"]},
        ],
        "audit_events": [
            {
                "id": str(item.id),
                "action": item.action,
                "resource_type": item.resource_type,
                "resource_id": item.resource_id,
                "created_at": item.created_at.isoformat(),
            }
            for item in audit_items
        ],
    }


@router.put("/governance/policy", response_model=TenantPolicyRead)
def update_governance_policy(
    payload: TenantPolicyUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationTenantPolicy:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    policy = ensure_policy(db, tenant_id, principal, lock=True)
    for field, value in payload.model_dump().items():
        setattr(policy, field, value)
    policy.updated_by = principal.subject
    db.add(record_audit(tenant_id, principal, "governance.policy_updated", "tenant_policy"))
    db.commit()
    db.refresh(policy)
    return policy


@router.get("/audit")
def list_audit_events(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationAuditEvent).where(AutomationAuditEvent.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationAuditEvent.created_at.desc()).offset(offset).limit(limit)
        )
    )
    return {
        "items": [
            {
                "id": str(item.id),
                "actor_subject": item.actor_subject,
                "action": item.action,
                "resource_type": item.resource_type,
                "resource_id": item.resource_id,
                "details": item.details,
                "created_at": item.created_at.isoformat(),
            }
            for item in items
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
