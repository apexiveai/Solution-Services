from fastapi import APIRouter

from app.modules.professional_services.common import (
    register_overview_route,
    register_resource_routes,
)
from app.modules.professional_services.integration.service import RESOURCES

router = APIRouter(
    prefix="/api/v1/professional-services/integration",
    tags=["Professional Services - Integration"],
)

for resource_path, (model, create_schema, read_schema, references) in RESOURCES.items():
    register_resource_routes(
        router,
        resource_path,
        model,
        create_schema,
        read_schema,
        references=references,
    )

register_overview_route(
    router,
    {resource_path.replace("-", "_"): resource[0] for resource_path, resource in RESOURCES.items()},
)