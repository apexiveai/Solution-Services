import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.automation.models import (
    AutomationBot,
    AutomationExecution,
    AutomationQueueItem,
)


def tenant_monitoring(db: Session, tenant_id: uuid.UUID) -> dict:
    bots = list(
        db.scalars(
            select(AutomationBot)
            .where(AutomationBot.tenant_id == tenant_id)
            .order_by(AutomationBot.name)
            .limit(100)
        )
    )
    executions = list(
        db.scalars(
            select(AutomationExecution)
            .where(
                AutomationExecution.tenant_id == tenant_id,
                AutomationExecution.status == "RUNNING",
            )
            .order_by(AutomationExecution.started_at.desc())
            .limit(100)
        )
    )
    queued = db.scalar(
        select(func.count(AutomationQueueItem.id)).where(
            AutomationQueueItem.tenant_id == tenant_id,
            AutomationQueueItem.status == "READY",
        )
    ) or 0
    return {
        "bots": bots,
        "running_executions": executions,
        "queued_executions": queued,
    }
