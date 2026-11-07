from fastapi import APIRouter, Depends

from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1", tags=["Identity"])


@router.get("/me")
def identity(principal: CurrentPrincipal = Depends(get_current_principal)) -> dict:
    return {
        "subject": principal.subject,
        "username": principal.username,
        "email": principal.email,
        "tenant_id": principal.tenant_id,
        "roles": principal.roles,
    }
