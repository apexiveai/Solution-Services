import uuid
from datetime import datetime
from decimal import Decimal
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


class OperationProjectCreate(ResourceCreate):
    project_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    operation_type: str = Field(min_length=1, max_length=64)
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None


class OperationProjectRead(OperationProjectCreate, ResourceRead):
    pass


class CustomerInsightCreate(ResourceCreate):
    customer_reference: str = Field(min_length=1, max_length=128)
    insight_type: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1)
    score: Decimal | None = None
    observed_at: datetime
    attributes: dict[str, Any] = Field(default_factory=dict)


class CustomerInsightRead(CustomerInsightCreate, ResourceRead):
    pass


class OperationCampaignCreate(ResourceCreate):
    campaign_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    channel: str = Field(min_length=1, max_length=48)
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    budget: Decimal | None = Field(default=None, ge=0)
    audience: dict[str, Any] = Field(default_factory=dict)


class OperationCampaignRead(OperationCampaignCreate, ResourceRead):
    pass


class OperationTaskCreate(ResourceCreate):
    project_id: uuid.UUID | None = None
    campaign_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    task_type: str = Field(min_length=1, max_length=64)
    assigned_to: str | None = Field(default=None, max_length=128)
    due_at: datetime | None = None
    completed_at: datetime | None = None


class OperationTaskRead(OperationTaskCreate, ResourceRead):
    pass


class OperationPerformanceCreate(ResourceCreate):
    metric_name: str = Field(min_length=1, max_length=96)
    value: Decimal
    unit: str | None = Field(default=None, max_length=32)
    period_start: datetime
    period_end: datetime | None = None
    dimensions: dict[str, Any] = Field(default_factory=dict)


class OperationPerformanceRead(OperationPerformanceCreate, ResourceRead):
    pass