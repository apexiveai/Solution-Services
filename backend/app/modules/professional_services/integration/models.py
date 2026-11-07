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


class IntegrationProject(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_projects"
    __table_args__ = (
        UniqueConstraint("tenant_id", "project_code", name="uq_ps_integration_project_code"),
        Index("ix_ps_integration_projects_tenant_status", "tenant_id", "status"),
    )

    project_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    integration_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_system: Mapped[str | None] = mapped_column(String(128))
    target_system: Mapped[str | None] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(Text)


class IntegrationSystem(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_systems"
    __table_args__ = (UniqueConstraint("tenant_id", "system_code", name="uq_ps_integration_system_code"),)

    system_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    system_type: Mapped[str] = mapped_column(String(64), nullable=False)
    environment: Mapped[str] = mapped_column(String(48), nullable=False, default="PRODUCTION")
    endpoint: Mapped[str | None] = mapped_column(String(500))
    configuration: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class IntegrationConnector(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_connectors"
    __table_args__ = (UniqueConstraint("tenant_id", "connector_code", name="uq_ps_connector_code"),)

    connector_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    connector_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_system_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    target_system_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    configuration: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class IntegrationAPI(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_apis"
    __table_args__ = (UniqueConstraint("tenant_id", "api_code", name="uq_ps_integration_api_code"),)

    api_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    protocol: Mapped[str] = mapped_column(String(24), nullable=False, default="REST")
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    authentication_type: Mapped[str] = mapped_column(String(48), nullable=False)
    credential_reference: Mapped[str | None] = mapped_column(String(200))
    specification: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class IntegrationDataMapping(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_data_mappings"
    __table_args__ = (UniqueConstraint("tenant_id", "mapping_code", name="uq_ps_mapping_code"),)

    mapping_code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_entity: Mapped[str] = mapped_column(String(128), nullable=False)
    target_entity: Mapped[str] = mapped_column(String(128), nullable=False)
    field_mappings: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    validation_rules: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)


class IntegrationSyncJob(
    ProfessionalServicesTenantMixin,
    ProfessionalServicesTimestampMixin,
    ProfessionalServicesRecordMixin,
    Base,
):
    __tablename__ = "ps_integration_sync_jobs"
    __table_args__ = (
        UniqueConstraint("tenant_id", "job_code", name="uq_ps_sync_job_code"),
        Index("ix_ps_sync_jobs_tenant_status", "tenant_id", "status"),
        Index("ix_ps_sync_jobs_tenant_started", "tenant_id", "started_at"),
    )

    job_code: Mapped[str] = mapped_column(String(64), nullable=False)
    connector_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    job_type: Mapped[str] = mapped_column(String(48), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    records_read: Mapped[int] = mapped_column(nullable=False, default=0)
    records_written: Mapped[int] = mapped_column(nullable=False, default=0)
    error_summary: Mapped[str | None] = mapped_column(Text)