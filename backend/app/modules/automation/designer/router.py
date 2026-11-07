from fastapi import APIRouter

from app.modules.automation.schemas import WorkflowValidate
from app.modules.automation.runtime.engine import SUPPORTED_ACTIONS
from app.security import CurrentPrincipal, get_current_principal
from fastapi import Depends

router = APIRouter(prefix="/designer", tags=["Automation Designer"])


@router.get("/actions")
def list_supported_actions(
    _: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    return {
        "actions": [
            {"type": action, "enabled": True}
            for action in SUPPORTED_ACTIONS
        ],
        "external_connectors": {
            "enabled": False,
            "detail": "External connector execution requires a separately approved adapter.",
        },
    }


@router.post("/validate")
def validate_workflow(
    payload: WorkflowValidate,
    _: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    return {
        "valid": True,
        "steps": len(payload.definition.get("steps", [])),
        "supported_actions": list(SUPPORTED_ACTIONS),
    }
