from app.modules.professional_services.integration.models import (
    IntegrationAPI,
    IntegrationConnector,
    IntegrationDataMapping,
    IntegrationProject,
    IntegrationSyncJob,
    IntegrationSystem,
)
from app.modules.professional_services.integration.schemas import (
    IntegrationAPICreate,
    IntegrationAPIRead,
    IntegrationConnectorCreate,
    IntegrationConnectorRead,
    IntegrationDataMappingCreate,
    IntegrationDataMappingRead,
    IntegrationProjectCreate,
    IntegrationProjectRead,
    IntegrationSyncJobCreate,
    IntegrationSyncJobRead,
    IntegrationSystemCreate,
    IntegrationSystemRead,
)

RESOURCES = {
    "projects": (IntegrationProject, IntegrationProjectCreate, IntegrationProjectRead, {}),
    "systems": (IntegrationSystem, IntegrationSystemCreate, IntegrationSystemRead, {}),
    "connectors": (
        IntegrationConnector,
        IntegrationConnectorCreate,
        IntegrationConnectorRead,
        {
            "source_system_id": IntegrationSystem,
            "target_system_id": IntegrationSystem,
        },
    ),
    "apis": (IntegrationAPI, IntegrationAPICreate, IntegrationAPIRead, {}),
    "data-mappings": (
        IntegrationDataMapping,
        IntegrationDataMappingCreate,
        IntegrationDataMappingRead,
        {},
    ),
    "sync-jobs": (
        IntegrationSyncJob,
        IntegrationSyncJobCreate,
        IntegrationSyncJobRead,
        {"connector_id": IntegrationConnector},
    ),
}