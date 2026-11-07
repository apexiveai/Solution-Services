from fastapi import APIRouter

from app.modules.telecom.routers.resource_management import (
    router as resource_management_router,
)

router = APIRouter(prefix="/api/arm")

router.include_router(resource_management_router)

__all__ = ["router"]