from app.modules.professional_services.operation.models import (
    CustomerInsight,
    OperationCampaign,
    OperationPerformance,
    OperationProject,
    OperationTask,
)
from app.modules.professional_services.operation.schemas import (
    CustomerInsightCreate,
    CustomerInsightRead,
    OperationCampaignCreate,
    OperationCampaignRead,
    OperationPerformanceCreate,
    OperationPerformanceRead,
    OperationProjectCreate,
    OperationProjectRead,
    OperationTaskCreate,
    OperationTaskRead,
)

RESOURCES = {
    "projects": (OperationProject, OperationProjectCreate, OperationProjectRead, {}),
    "customer-insights": (CustomerInsight, CustomerInsightCreate, CustomerInsightRead, {}),
    "campaigns": (OperationCampaign, OperationCampaignCreate, OperationCampaignRead, {}),
    "tasks": (
        OperationTask,
        OperationTaskCreate,
        OperationTaskRead,
        {
            "project_id": OperationProject,
            "campaign_id": OperationCampaign,
        },
    ),
    "performance": (
        OperationPerformance,
        OperationPerformanceCreate,
        OperationPerformanceRead,
        {},
    ),
}