import logging
import time
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.modules.automation.dependencies import record_audit
from app.modules.automation.models import (
    AutomationBot,
    AutomationExecution,
    AutomationQueueItem,
    AutomationSchedule,
    AutomationWorkflow,
)
from app.modules.automation.scheduler.service import next_schedule_run
from app.modules.automation.service import enqueue_workflow, run_execution
from app.security import CurrentPrincipal

logger = logging.getLogger("aeop.automation.worker")


def _system_principal(tenant_id) -> CurrentPrincipal:
    return CurrentPrincipal(
        subject="core-rpa-worker",
        tenant_id=str(tenant_id),
        roles=["admin", "operator"],
        claims={"service": "core-rpa-worker"},
    )


def dispatch_due_schedules(db: Session, now: datetime | None = None) -> int:
    current_time = now or datetime.now(timezone.utc)
    schedules = list(
        db.scalars(
            select(AutomationSchedule)
            .where(
                AutomationSchedule.enabled.is_(True),
                AutomationSchedule.next_run_at.is_not(None),
                AutomationSchedule.next_run_at <= current_time,
            )
            .order_by(AutomationSchedule.next_run_at)
            .with_for_update(skip_locked=True)
            .limit(25)
        )
    )
    dispatched = 0
    for schedule in schedules:
        principal = _system_principal(schedule.tenant_id)
        workflow = db.scalar(
            select(AutomationWorkflow).where(
                AutomationWorkflow.id == schedule.workflow_id,
                AutomationWorkflow.tenant_id == schedule.tenant_id,
            )
        )
        if workflow is None or workflow.status != "PUBLISHED":
            schedule.enabled = False
            db.add(
                record_audit(
                    schedule.tenant_id,
                    principal,
                    "schedule.disabled",
                    "schedule",
                    schedule.id,
                    {"reason": "workflow is not published"},
                )
            )
            db.commit()
            continue

        try:
            enqueue_workflow(
                db,
                workflow,
                schedule.tenant_id,
                principal,
                {},
                priority=5,
            )
        except HTTPException as exc:
            schedule.last_run_at = current_time
            schedule.next_run_at = next_schedule_run(
                schedule.cron_expression,
                schedule.timezone_name,
                current_time,
            )
            db.add(
                record_audit(
                    schedule.tenant_id,
                    principal,
                    "schedule.dispatch_rejected",
                    "schedule",
                    schedule.id,
                    {"reason": exc.detail, "status_code": exc.status_code},
                )
            )
            db.commit()
            logger.warning("Schedule %s was skipped: %s", schedule.id, exc.detail)
            continue

        schedule.last_run_at = current_time
        schedule.next_run_at = next_schedule_run(
            schedule.cron_expression,
            schedule.timezone_name,
            current_time,
        )
        db.add(record_audit(schedule.tenant_id, principal, "schedule.dispatched", "schedule", schedule.id))
        db.commit()
        dispatched += 1
    return dispatched


def process_queue_once(db: Session) -> bool:
    workflow_runtime = AutomationWorkflow.definition["runtime"].as_string()
    queue_item = db.scalar(
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
            AutomationQueueItem.status == "READY",
            AutomationQueueItem.available_at <= datetime.now(timezone.utc),
            or_(workflow_runtime.is_(None), workflow_runtime == "CORE"),
        )
        .order_by(AutomationQueueItem.priority.asc(), AutomationQueueItem.created_at.asc())
        .with_for_update(skip_locked=True, of=AutomationQueueItem)
        .limit(1)
    )
    if queue_item is None:
        db.rollback()
        return False

    execution = db.scalar(
        select(AutomationExecution).where(
            AutomationExecution.id == queue_item.execution_id,
            AutomationExecution.tenant_id == queue_item.tenant_id,
        )
    )
    if execution is None or execution.status != "QUEUED":
        queue_item.status = "DEAD"
        db.commit()
        return True

    workflow = db.scalar(
        select(AutomationWorkflow).where(
            AutomationWorkflow.id == execution.workflow_id,
            AutomationWorkflow.tenant_id == execution.tenant_id,
        )
    )
    if workflow is None:
        queue_item.status = "DEAD"
        execution.status = "FAILED"
        execution.error_message = "Workflow definition is unavailable."
        execution.finished_at = datetime.now(timezone.utc)
        db.commit()
        return True

    bot = db.scalar(
        select(AutomationBot)
        .where(
            AutomationBot.tenant_id == execution.tenant_id,
            AutomationBot.status == "IDLE",
        )
        .order_by(AutomationBot.created_at)
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    if bot is None:
        db.rollback()
        return False
    principal = _system_principal(execution.tenant_id)
    try:
        run_execution(db, execution, workflow, principal, bot)
    except HTTPException as exc:
        db.rollback()
        retry_item = db.scalar(
            select(AutomationQueueItem).where(
                AutomationQueueItem.id == queue_item.id,
                AutomationQueueItem.tenant_id == queue_item.tenant_id,
                AutomationQueueItem.status == "READY",
            )
        )
        if retry_item is not None:
            retry_item.available_at = datetime.now(timezone.utc) + timedelta(minutes=1)
            db.commit()
        logger.warning("Execution %s was deferred: %s", execution.id, exc.detail)
    return True


def run_once() -> int:
    with SessionLocal() as db:
        scheduled = dispatch_due_schedules(db)
        if process_queue_once(db):
            return scheduled + 1
        return scheduled


def run_forever(poll_interval_seconds: float = 2.0) -> None:
    if poll_interval_seconds <= 0 or poll_interval_seconds > 60:
        raise ValueError("Worker polling interval must be between 0 and 60 seconds.")
    while True:
        try:
            processed = run_once()
            if not processed:
                time.sleep(poll_interval_seconds)
        except SQLAlchemyError:
            logger.exception("Automation worker database operation failed")
            time.sleep(poll_interval_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_forever()
