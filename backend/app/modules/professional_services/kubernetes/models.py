import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, JSON, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.modules.professional_services.common import (
    ProfessionalServicesRecordMixin,
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
)


class KubernetesCluster(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_clusters"
    __table_args__ = (
        UniqueConstraint("tenant_id", "cluster_code", name="uq_ps_k8s_cluster_code"),
        Index("ix_ps_k8s_clusters_tenant_status", "tenant_id", "status"),
    )

    cluster_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    environment: Mapped[str] = mapped_column(String(48), nullable=False)
    region: Mapped[str | None] = mapped_column(String(100))
    kubernetes_version: Mapped[str | None] = mapped_column(String(32))
    api_endpoint: Mapped[str | None] = mapped_column(String(500))
    credential_reference: Mapped[str | None] = mapped_column(String(200))


class KubernetesNode(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_nodes"
    __table_args__ = (Index("ix_ps_k8s_nodes_tenant_cluster", "tenant_id", "cluster_id"),)

    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    node_name: Mapped[str] = mapped_column(String(200), nullable=False)
    node_pool: Mapped[str | None] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(48), nullable=False, default="WORKER")
    cpu_capacity: Mapped[str | None] = mapped_column(String(32))
    memory_capacity: Mapped[str | None] = mapped_column(String(32))
    labels: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class KubernetesNamespace(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_namespaces"
    __table_args__ = (
        UniqueConstraint("tenant_id", "cluster_id", "name", name="uq_ps_k8s_namespace_name"),
        Index("ix_ps_k8s_namespaces_tenant_cluster", "tenant_id", "cluster_id"),
    )

    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    labels: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    resource_quota: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class KubernetesWorkload(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_workloads"
    __table_args__ = (Index("ix_ps_k8s_workloads_tenant_cluster", "tenant_id", "cluster_id"),)

    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    namespace_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    workload_type: Mapped[str] = mapped_column(String(48), nullable=False)
    image: Mapped[str | None] = mapped_column(String(500))
    replicas: Mapped[int] = mapped_column(nullable=False, default=1)
    resource_requests: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class KubernetesDeployment(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_deployments"
    __table_args__ = (Index("ix_ps_k8s_deployments_tenant_cluster", "tenant_id", "cluster_id"),)

    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    workload_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    namespace_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str | None] = mapped_column(String(64))
    desired_replicas: Mapped[int] = mapped_column(nullable=False, default=1)
    available_replicas: Mapped[int] = mapped_column(nullable=False, default=0)
    rollout_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rollout_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    manifest: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class KubernetesMigration(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_migrations"
    __table_args__ = (Index("ix_ps_k8s_migrations_tenant_status", "tenant_id", "status"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    migration_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_environment: Mapped[str] = mapped_column(String(200), nullable=False)
    target_cluster_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    planned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    migration_plan: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class KubernetesMaintenance(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_kubernetes_maintenance"
    __table_args__ = (Index("ix_ps_k8s_maintenance_tenant_cluster", "tenant_id", "cluster_id"),)

    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    maintenance_type: Mapped[str] = mapped_column(String(64), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    summary: Mapped[str | None] = mapped_column(Text)
    maintenance_plan: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)