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


class IntegrationProjectCreate(ResourceCreate):
    project_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    integration_type: str = Field(min_length=1, max_length=64)
    source_system: str | None = Field(default=None, max_length=128)
    target_system: str | None = Field(default=None, max_length=128)
    description: str | None = None


class IntegrationProjectRead(IntegrationProjectCreate, ResourceRead):
    pass


class IntegrationSystemCreate(ResourceCreate):
    system_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    system_type: str = Field(min_length=1, max_length=64)
    environment: str = Field(default="PRODUCTION", min_length=1, max_length=48)
    endpoint: str | None = Field(default=None, max_length=500)
    configuration: dict[str, Any] = Field(default_factory=dict)


class IntegrationSystemRead(IntegrationSystemCreate, ResourceRead):
    pass


class IntegrationConnectorCreate(ResourceCreate):
    connector_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    connector_type: str = Field(min_length=1, max_length=64)
    source_system_id: uuid.UUID | None = None
    target_system_id: uuid.UUID | None = None
    configuration: dict[str, Any] = Field(default_factory=dict)


class IntegrationConnectorRead(IntegrationConnectorCreate, ResourceRead):
    pass


class IntegrationAPICreate(ResourceCreate):
    api_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    protocol: str = Field(default="REST", min_length=1, max_length=24)
    base_url: str = Field(min_length=1, max_length=500)
    authentication_type: str = Field(min_length=1, max_length=48)
    credential_reference: str | None = Field(default=None, max_length=200)
    specification: dict[str, Any] = Field(default_factory=dict)


class IntegrationAPIRead(IntegrationAPICreate, ResourceRead):
    pass


class IntegrationDataMappingCreate(ResourceCreate):
    mapping_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    source_entity: str = Field(min_length=1, max_length=128)
    target_entity: str = Field(min_length=1, max_length=128)
    field_mappings: list[dict[str, Any]] = Field(default_factory=list)
    validation_rules: list[dict[str, Any]] = Field(default_factory=list)


class IntegrationDataMappingRead(IntegrationDataMappingCreate, ResourceRead):
    pass


class IntegrationSyncJobCreate(ResourceCreate):
    job_code: str = Field(min_length=1, max_length=64)
    connector_id: uuid.UUID | None = None
    job_type: str = Field(min_length=1, max_length=48)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    records_read: int = Field(default=0, ge=0)
    records_written: int = Field(default=0, ge=0)
    error_summary: str | None = None


class IntegrationSyncJobRead(IntegrationSyncJobCreate, ResourceRead):
    pass