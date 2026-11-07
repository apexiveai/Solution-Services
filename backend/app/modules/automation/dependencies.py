import uuid

from fastapi import HTTPException, status

from app.security import CurrentPrincipal
from app.modules.automation.models import AutomationAuditEvent


ROLE_ALIASES = {
    "admin": {"admin", "administrator"},
    "developer": {"developer"},
    "operator": {"operator"},
    "viewer": {"viewer"},
    "agent": {"core_rpa_agent"},
}


def tenant_uuid(principal: CurrentPrincipal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token contains an invalid tenant_id claim",
        ) from exc


def require_automation_role(principal: CurrentPrincipal, *allowed_roles: str) -> None:
    roles = {role.casefold() for role in principal.roles}
    allowed = set().union(*(ROLE_ALIASES.get(role, {role}) for role in allowed_roles))
    if not roles.intersection(allowed):
        raise HTTPException(status_code=403, detail="Insufficient automation role permissions")


def record_audit(
    tenant_id: uuid.UUID,
    principal: CurrentPrincipal,
    action: str,
    resource_type: str,
    resource_id: uuid.UUID | None = None,
    details: dict | None = None,
) -> AutomationAuditEvent:
    return AutomationAuditEvent(
        tenant_id=tenant_id,
        actor_subject=principal.subject,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id else None,
        details=details or {},
    )
