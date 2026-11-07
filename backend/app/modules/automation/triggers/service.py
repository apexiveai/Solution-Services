from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.automation.models import AutomationTrigger


def get_enabled_trigger(
    db: Session,
    tenant_id,
    trigger_id,
) -> AutomationTrigger | None:
    return db.scalar(
        select(AutomationTrigger).where(
            AutomationTrigger.id == trigger_id,
            AutomationTrigger.tenant_id == tenant_id,
            AutomationTrigger.enabled.is_(True),
        )
    )
