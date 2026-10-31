import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ServiceCaseCreate(BaseModel):
    case_number: str = Field(min_length=1, max_length=64)
    service_code: str = Field(min_length=1, max_length=64)
    subject: str = Field(min_length=1, max_length=240)
    requester_reference: str | None = Field(default=None, max_length=128)
    description: str | None = None
    priority: str = Field(default="NORMAL", max_length=24)
    details: dict[str, Any] = Field(default_factory=dict)


class ServiceCaseRead(ServiceCaseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    assigned_to: str | None
    created_at: datetime
    updated_at: datetime


class EmergencyIncidentCreate(BaseModel):
    incident_number: str = Field(min_length=1, max_length=64)
    incident_type: str = Field(min_length=1, max_length=48)
    source: str = Field(default="DISPATCH", max_length=32)
    severity: str = Field(default="MEDIUM", max_length=24)
    location: dict[str, Any] = Field(default_factory=dict)
    description: str | None = None


class EmergencyIncidentRead(EmergencyIncidentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    reported_at: datetime | None
    created_at: datetime
    updated_at: datetime
