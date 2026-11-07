import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

DeploymentEnvironment = Literal["DEVELOPMENT", "STAGING", "PRODUCTION"]
DeploymentStatus = Literal["PLANNED", "ACTIVE", "PAUSED", "RETIRED"]


class ProductDeploymentCreate(BaseModel):
    product_code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=160)
    environment: DeploymentEnvironment = "DEVELOPMENT"
    configuration: dict[str, Any] = Field(default_factory=dict)
    integrations: list[str] = Field(default_factory=list, max_length=40)


class ProductDeploymentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    environment: DeploymentEnvironment | None = None
    status: DeploymentStatus | None = None
    configuration: dict[str, Any] | None = None
    integrations: list[str] | None = Field(default=None, max_length=40)


class ProductDeploymentRead(ProductDeploymentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: DeploymentStatus
    created_at: datetime
    updated_at: datetime
