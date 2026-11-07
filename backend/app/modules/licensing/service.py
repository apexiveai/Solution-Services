import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.automation.models import AutomationBot, AutomationExecution
from app.modules.licensing.models import CoreRpaDeveloperSeat, CoreRpaLicense


def tenant_uuid(principal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=403, detail="Token contains an invalid tenant_id claim") from exc


def require_sales_role(principal) -> None:
    sales_roles = {"sales", "sales_admin", "platform_admin", "system_admin", "super_admin"}
    if not sales_roles.intersection(role.casefold() for role in principal.roles):
        raise HTTPException(status_code=403, detail="Sales authorization is required")


def get_active_license(db: Session, tenant_id: uuid.UUID) -> CoreRpaLicense | None:
    now = datetime.now(timezone.utc)
    return db.scalar(
        select(CoreRpaLicense)
        .where(
            CoreRpaLicense.tenant_id == tenant_id,
            CoreRpaLicense.status == "ACTIVE",
            CoreRpaLicense.starts_at <= now,
            CoreRpaLicense.expires_at > now,
        )
        .order_by(CoreRpaLicense.expires_at.desc())
        .limit(1)
    )


def require_active_license(db: Session, tenant_id: uuid.UUID) -> CoreRpaLicense:
    license_record = get_active_license(db, tenant_id)
    if license_record is None:
        raise HTTPException(
            status_code=402,
            detail="An active Apexive CoreRPA license is required for this operation",
        )
    return license_record


def enforce_bot_entitlement(db: Session, tenant_id: uuid.UUID) -> None:
    license_record = require_active_license(db, tenant_id)
    registered_bots = db.scalar(
        select(func.count(AutomationBot.id)).where(AutomationBot.tenant_id == tenant_id)
    ) or 0
    if registered_bots >= license_record.bot_limit:
        raise HTTPException(status_code=429, detail="Licensed CoreRPA bot limit reached")


def enforce_execution_entitlement(db: Session, tenant_id: uuid.UUID) -> None:
    license_record = require_active_license(db, tenant_id)
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    executions = db.scalar(
        select(func.count(AutomationExecution.id)).where(
            AutomationExecution.tenant_id == tenant_id,
            AutomationExecution.created_at >= month_start,
        )
    ) or 0
    if executions >= license_record.monthly_execution_limit:
        raise HTTPException(status_code=429, detail="Licensed monthly execution limit reached")


def require_developer_seat(
    db: Session,
    tenant_id: uuid.UUID,
    subject: str,
    roles: list[str],
) -> None:
    normalized_roles = {role.casefold() for role in roles}
    if "admin" in normalized_roles or "administrator" in normalized_roles:
        return
    if "developer" not in normalized_roles:
        return
    seat = db.scalar(
        select(CoreRpaDeveloperSeat.id).where(
            CoreRpaDeveloperSeat.tenant_id == tenant_id,
            CoreRpaDeveloperSeat.subject == subject,
        )
    )
    if seat is None:
        raise HTTPException(status_code=403, detail="An assigned CoreRPA developer seat is required")
