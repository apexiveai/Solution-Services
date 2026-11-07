from app.modules.professional_services.consultation.models import (
    ConsultationAssessment,
    ConsultationDeliverable,
    ConsultationProject,
    ConsultationRoadmap,
    ConsultationStrategy,
)
from app.modules.professional_services.consultation.schemas import (
    ConsultationAssessmentCreate,
    ConsultationAssessmentRead,
    ConsultationDeliverableCreate,
    ConsultationDeliverableRead,
    ConsultationProjectCreate,
    ConsultationProjectRead,
    ConsultationRoadmapCreate,
    ConsultationRoadmapRead,
    ConsultationStrategyCreate,
    ConsultationStrategyRead,
)

RESOURCES = {
    "projects": (ConsultationProject, ConsultationProjectCreate, ConsultationProjectRead, {}),
    "assessments": (
        ConsultationAssessment,
        ConsultationAssessmentCreate,
        ConsultationAssessmentRead,
        {"project_id": ConsultationProject},
    ),
    "strategies": (
        ConsultationStrategy,
        ConsultationStrategyCreate,
        ConsultationStrategyRead,
        {"project_id": ConsultationProject},
    ),
    "roadmaps": (
        ConsultationRoadmap,
        ConsultationRoadmapCreate,
        ConsultationRoadmapRead,
        {"project_id": ConsultationProject},
    ),
    "deliverables": (
        ConsultationDeliverable,
        ConsultationDeliverableCreate,
        ConsultationDeliverableRead,
        {"project_id": ConsultationProject},
    ),
}