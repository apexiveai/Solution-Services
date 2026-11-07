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


class KubernetesClusterCreate(ResourceCreate):
    cluster_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    provider: str = Field(min_length=1, max_length=64)
    environment: str = Field(min_length=1, max_length=48)
    region: str | None = Field(default=None, max_length=100)
    kubernetes_version: str | None = Field(default=None, max_length=32)
    api_endpoint: str | None = Field(default=None, max_length=500)
    credential_reference: str | None = Field(default=None, max_length=200)


class KubernetesClusterRead(KubernetesClusterCreate, ResourceRead):
    pass


class KubernetesNodeCreate(ResourceCreate):
    cluster_id: uuid.UUID
    node_name: str = Field(min_length=1, max_length=200)
    node_pool: str | None = Field(default=None, max_length=100)
    role: str = Field(default="WORKER", min_length=1, max_length=48)
    cpu_capacity: str | None = Field(default=None, max_length=32)
    memory_capacity: str | None = Field(default=None, max_length=32)
    labels: dict[str, Any] = Field(default_factory=dict)


class KubernetesNodeRead(KubernetesNodeCreate, ResourceRead):
    pass


class KubernetesNamespaceCreate(ResourceCreate):
    cluster_id: uuid.UUID
    name: str = Field(min_length=1, max_length=128)
    labels: dict[str, Any] = Field(default_factory=dict)
    resource_quota: dict[str, Any] = Field(default_factory=dict)


class KubernetesNamespaceRead(KubernetesNamespaceCreate, ResourceRead):
    pass


class KubernetesWorkloadCreate(ResourceCreate):
    cluster_id: uuid.UUID
    namespace_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    workload_type: str = Field(min_length=1, max_length=48)
    image: str | None = Field(default=None, max_length=500)
    replicas: int = Field(default=1, ge=0)
    resource_requests: dict[str, Any] = Field(default_factory=dict)


class KubernetesWorkloadRead(KubernetesWorkloadCreate, ResourceRead):
    pass


class KubernetesDeploymentCreate(ResourceCreate):
    cluster_id: uuid.UUID
    workload_id: uuid.UUID | None = None
    namespace_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    version: str | None = Field(default=None, max_length=64)
    desired_replicas: int = Field(default=1, ge=0)
    available_replicas: int = Field(default=0, ge=0)
    rollout_started_at: datetime | None = None
    rollout_completed_at: datetime | None = None
    manifest: dict[str, Any] = Field(default_factory=dict)


class KubernetesDeploymentRead(KubernetesDeploymentCreate, ResourceRead):
    pass


class KubernetesMigrationCreate(ResourceCreate):
    name: str = Field(min_length=1, max_length=200)
    migration_type: str = Field(min_length=1, max_length=64)
    source_environment: str = Field(min_length=1, max_length=200)
    target_cluster_id: uuid.UUID | None = None
    planned_at: datetime | None = None
    completed_at: datetime | None = None
    migration_plan: dict[str, Any] = Field(default_factory=dict)


class KubernetesMigrationRead(KubernetesMigrationCreate, ResourceRead):
    pass


class KubernetesMaintenanceCreate(ResourceCreate):
    cluster_id: uuid.UUID
    maintenance_type: str = Field(min_length=1, max_length=64)
    scheduled_at: datetime
    completed_at: datetime | None = None
    summary: str | None = None
    maintenance_plan: dict[str, Any] = Field(default_factory=dict)


class KubernetesMaintenanceRead(KubernetesMaintenanceCreate, ResourceRead):
    pass