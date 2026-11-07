import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="PLANNED", min_length=1, max_length=32)
    details: dict[str, Any] = Field(default_factory=dict)


class ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ConsultationProjectCreate(ResourceCreate):
    project_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    project_type: str = Field(min_length=1, max_length=64)
    client_reference: str | None = Field(default=None, max_length=128)
    description: str | None = None


class ConsultationProjectRead(ConsultationProjectCreate, ResourceRead):
    pass


class ConsultationAssessmentCreate(ResourceCreate):
    project_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    assessment_type: str = Field(min_length=1, max_length=64)
    assessed_at: datetime | None = None
    findings: dict[str, Any] = Field(default_factory=dict)


class ConsultationAssessmentRead(ConsultationAssessmentCreate, ResourceRead):
    pass


class ConsultationStrategyCreate(ResourceCreate):
    project_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    strategy_type: str = Field(min_length=1, max_length=64)
    effective_from: datetime | None = None
    objectives: list[Any] = Field(default_factory=list)


class ConsultationStrategyRead(ConsultationStrategyCreate, ResourceRead):
    pass


class ConsultationRoadmapCreate(ResourceCreate):
    project_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    starts_at: datetime | None = None
    target_completion_at: datetime | None = None
    milestones: list[Any] = Field(default_factory=list)


class ConsultationRoadmapRead(ConsultationRoadmapCreate, ResourceRead):
    pass


class ConsultationDeliverableCreate(ResourceCreate):
    project_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    deliverable_type: str = Field(min_length=1, max_length=64)
    due_at: datetime | None = None
    delivered_at: datetime | None = None


class ConsultationDeliverableRead(ConsultationDeliverableCreate, ResourceRead):
    pass