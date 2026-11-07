from fastapi import APIRouter

from app.modules.professional_services.consultation.router import (
    router as consultation_router,
)
from app.modules.professional_services.integration.router import (
    router as integration_router,
)
from app.modules.professional_services.kubernetes.router import (
    router as kubernetes_router,
)
from app.modules.professional_services.operation.router import router as operation_router

router = APIRouter()
router.include_router(consultation_router)
router.include_router(operation_router)
router.include_router(integration_router)
router.include_router(kubernetes_router)