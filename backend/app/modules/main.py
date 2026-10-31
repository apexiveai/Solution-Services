from fastapi import APIRouter

from app.modules.manufacturing import router as manufacturing_router
from app.modules.manufacturing import models as _manufacturing_models  # noqa: F401
from app.modules.public_services import router as public_services_router
from app.modules.public_services import models as _public_services_models  # noqa: F401

router = APIRouter()
router.include_router(public_services_router)
router.include_router(manufacturing_router)

__all__ = ["router"]