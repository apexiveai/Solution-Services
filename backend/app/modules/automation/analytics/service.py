from datetime import datetime, time, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.automation.models import AutomationExecution


def execution_analytics(db: Session, tenant_id) -> dict:
    start_of_day = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)
    statuses = db.execute(
        select(AutomationExecution.status, func.count(AutomationExecution.id))
        .where(
            AutomationExecution.tenant_id == tenant_id,
            AutomationExecution.created_at >= start_of_day,
        )
        .group_by(AutomationExecution.status)
    ).all()
    by_status = dict(statuses)
    completed = by_status.get("SUCCEEDED", 0) + by_status.get("FAILED", 0)
    failed = by_status.get("FAILED", 0)
    return {
        "executions_today": sum(by_status.values()),
        "executions_by_status": by_status,
        "failure_rate": round(failed / completed, 4) if completed else 0,
    }
