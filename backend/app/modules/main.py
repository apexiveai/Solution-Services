from fastapi import APIRouter

from app.modules.manufacturing import router as manufacturing_router
from app.modules.manufacturing import models as _manufacturing_models  # noqa: F401
from app.modules.public_services import router as public_services_router
from app.modules.public_services import models as _public_services_models  # noqa: F401
from app.modules.professional_services import router as professional_services_router
from app.modules.professional_services.consultation import models as _consultation_models  # noqa: F401
from app.modules.professional_services.integration import models as _integration_models  # noqa: F401
from app.modules.professional_services.kubernetes import models as _kubernetes_models  # noqa: F401
from app.modules.professional_services.operation import models as _operation_models  # noqa: F401
from app.modules.products import router as products_router
from app.modules.products import models as _product_models  # noqa: F401
from app.modules.automation import router as automation_router
from app.modules.automation import models as _automation_models  # noqa: F401
from app.modules.licensing import router as licensing_router
from app.modules.licensing import models as _licensing_models  # noqa: F401

router = APIRouter()
router.include_router(public_services_router)
router.include_router(manufacturing_router)
router.include_router(professional_services_router)
router.include_router(products_router)
router.include_router(automation_router)
router.include_router(licensing_router)

__all__ = ["router"]