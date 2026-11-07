import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.dependencies import record_audit, require_automation_role, tenant_uuid
from app.modules.automation.models import AutomationWorkflow, AutomationWorkflowVersion
from app.modules.automation.schemas import WorkflowCreate, WorkflowRead, WorkflowUpdate
from app.modules.automation.service import get_tenant_resource
from app.modules.licensing.service import require_active_license, require_developer_seat
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/workflows", tags=["Automation Workflows"])


@router.get("")
def list_workflows(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    statement = select(AutomationWorkflow).where(AutomationWorkflow.tenant_id == tenant_id)
    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = list(
        db.scalars(
            statement.order_by(AutomationWorkflow.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )
    return {
        "items": [WorkflowRead.model_validate(item).model_dump(mode="json") for item in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
def create_workflow(
    payload: WorkflowCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationWorkflow:
    require_automation_role(principal, "admin", "developer")
    tenant_id = tenant_uuid(principal)
    require_developer_seat(db, tenant_id, principal.subject, principal.roles)
    require_active_license(db, tenant_id)
    workflow = AutomationWorkflow(
        tenant_id=tenant_id,
        name=payload.name.strip(),
        description=payload.description,
        definition=payload.definition,
        requires_approval=payload.requires_approval,
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
        db.add(record_audit(tenant_id, principal, "workflow.created", "workflow", workflow.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A workflow with this name already exists") from exc
    db.refresh(workflow)
    return workflow


@router.get("/{workflow_id}", response_model=WorkflowRead)
def get_workflow(
    workflow_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationWorkflow:
    return get_tenant_resource(db, AutomationWorkflow, workflow_id, tenant_uuid(principal))


@router.get("/{workflow_id}/versions")
def list_workflow_versions(
    workflow_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[dict]:
    tenant_id = tenant_uuid(principal)
    require_developer_seat(db, tenant_id, principal.subject, principal.roles)
    require_active_license(db, tenant_id)
    get_tenant_resource(db, AutomationWorkflow, workflow_id, tenant_id)
    versions = db.scalars(
        select(AutomationWorkflowVersion)
        .where(
            AutomationWorkflowVersion.tenant_id == tenant_id,
            AutomationWorkflowVersion.workflow_id == workflow_id,
        )
        .order_by(AutomationWorkflowVersion.version.desc())
    )
    return [
        {
            "version": version.version,
            "definition": version.definition,
            "actor_subject": version.actor_subject,
            "created_at": version.created_at,
        }
        for version in versions
    ]


@router.patch("/{workflow_id}", response_model=WorkflowRead)
def update_workflow(
    workflow_id: uuid.UUID,
    payload: WorkflowUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> AutomationWorkflow:
    require_automation_role(principal, "admin", "developer")
    updates = payload.model_dump(exclude_unset=True)
    if not updates or any(value is None for value in updates.values()):
        raise HTTPException(status_code=422, detail="Provide at least one non-null workflow field")

    tenant_id = tenant_uuid(principal)
    workflow = get_tenant_resource(db, AutomationWorkflow, workflow_id, tenant_id)
    if workflow.status == "ARCHIVED":
        raise HTTPException(status_code=409, detail="Archived workflows cannot be changed")
    for field, value in updates.items():
        if field == "name":
            value = value.strip()
        setattr(workflow, field, value)
    workflow.version += 1
    db.add(
        AutomationWorkflowVersion(
            tenant_id=tenant_id,
            workflow_id=workflow.id,
            version=workflow.version,
            definition=workflow.definition,
            actor_subject=principal.subject,
        )
    )
    db.add(record_audit(tenant_id, principal, "workflow.updated", "workflow", workflow.id))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A workflow with this name already exists") from exc
    db.refresh(workflow)
    return workflow
