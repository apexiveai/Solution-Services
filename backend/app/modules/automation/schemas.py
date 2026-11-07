import uuid
import json
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator

from app.modules.automation.runtime.engine import validate_definition


WorkflowStatus = Literal["DRAFT", "PUBLISHED", "ARCHIVED"]
BotStatus = Literal["OFFLINE", "IDLE", "BUSY", "PAUSED"]
ConnectorType = Literal["REST_API", "BROWSER", "DATABASE", "FILES", "DOCUMENTS", "DESKTOP", "EMAIL"]


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=1000)
    definition: dict[str, Any] = Field(default_factory=lambda: {"steps": []})
    requires_approval: bool = False

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, definition: dict[str, Any]) -> dict[str, Any]:
        validate_definition(definition)
        return definition


class WorkflowUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=1000)
    definition: dict[str, Any] | None = None
    requires_approval: bool | None = None
    status: WorkflowStatus | None = None

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, definition: dict[str, Any] | None) -> dict[str, Any] | None:
        if definition is not None:
            validate_definition(definition)
        return definition


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: str
    definition: dict[str, Any]
    version: int
    status: WorkflowStatus
    requires_approval: bool
    created_by: str
    created_at: datetime
    updated_at: datetime


class WorkflowValidate(BaseModel):
    definition: dict[str, Any] = Field(default_factory=lambda: {"steps": []})

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, definition: dict[str, Any]) -> dict[str, Any]:
        validate_definition(definition)
        return definition


class BotCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    capabilities: list[str] = Field(default_factory=list, max_length=40)
    worker_version: str | None = Field(default=None, max_length=80)


class BotControl(BaseModel):
    action: Literal["START", "STOP", "PAUSE", "RESUME"]


class BotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    status: BotStatus
    capabilities: list[str]
    worker_version: str | None
    registered_by: str
    last_heartbeat_at: datetime | None
    created_at: datetime
    updated_at: datetime


class RunCreate(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=5, ge=1, le=10)


class RunExecution(BaseModel):
    bot_id: uuid.UUID | None = None


class ExecutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    workflow_id: uuid.UUID
    workflow_version: int
    bot_id: uuid.UUID | None
    status: str
    input_data: dict[str, Any]
    result_data: dict[str, Any] | None
    error_message: str | None
    requested_by: str
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime


class RuntimeClaimRead(BaseModel):
    execution_id: uuid.UUID
    tenant_id: uuid.UUID
    workflow_id: uuid.UUID
    workflow_version: int
    claim_attempt: int = Field(ge=1)
    contract_version: Literal[1]
    runtime: Literal["AIS", "CY"]
    definition: dict[str, Any]
    input_data: dict[str, Any]


class RuntimeCompletionCreate(BaseModel):
    claim_attempt: int = Field(ge=1)
    status: Literal["SUCCEEDED", "FAILED"]
    result_data: dict[str, Any] | None = None
    error_message: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def validate_result(self) -> "RuntimeCompletionCreate":
        if self.status == "SUCCEEDED" and self.result_data is None:
            raise ValueError("Successful executions require result_data.")
        if self.status == "FAILED" and not self.error_message:
            raise ValueError("Failed executions require an error_message.")
        if self.result_data is not None:
            try:
                encoded = json.dumps(self.result_data, allow_nan=False).encode("utf-8")
            except (TypeError, ValueError) as exc:
                raise ValueError("result_data must contain valid JSON values.") from exc
            if len(encoded) > 1_000_000:
                raise ValueError("result_data cannot exceed 1 MB.")
        return self


class QueueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    execution_id: uuid.UUID
    priority: int
    status: str
    attempts: int
    available_at: datetime
    created_at: datetime


class ScheduleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    workflow_id: uuid.UUID
    cron_expression: str = Field(min_length=5, max_length=120)
    timezone_name: str = Field(default="UTC", min_length=1, max_length=80)
    enabled: bool = True


class ScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    workflow_id: uuid.UUID
    name: str
    cron_expression: str
    timezone_name: str
    enabled: bool
    next_run_at: datetime | None
    last_run_at: datetime | None
    created_by: str
    created_at: datetime


class TriggerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    workflow_id: uuid.UUID
    event_name: str = Field(min_length=1, max_length=120)
    enabled: bool = True


class TriggerFire(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)


class EnabledUpdate(BaseModel):
    enabled: bool


class TriggerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    workflow_id: uuid.UUID
    name: str
    event_name: str
    enabled: bool
    created_by: str
    created_at: datetime


class ApprovalDecision(BaseModel):
    decision: Literal["APPROVED", "REJECTED"]
    note: str | None = Field(default=None, max_length=1000)


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    execution_id: uuid.UUID
    status: str
    requested_by: str
    reviewed_by: str | None
    review_note: str | None
    created_at: datetime
    reviewed_at: datetime | None


class IntegrationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    connector_type: ConnectorType
    approved_hosts: list[str] = Field(default_factory=list, max_length=50)
    credential_id: uuid.UUID | None = None

    @field_validator("approved_hosts")
    @classmethod
    def validate_hosts(cls, hosts: list[str]) -> list[str]:
        normalized = [host.strip().lower() for host in hosts]
        if any(not host or "/" in host or "@" in host for host in normalized):
            raise ValueError("Approved targets must be host names, not URLs or credentials.")
        return normalized


class IntegrationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    connector_type: ConnectorType
    approved_hosts: list[str]
    credential_id: uuid.UUID | None
    enabled: bool
    created_by: str
    created_at: datetime


class TemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=1000)
    category: str = Field(min_length=1, max_length=80)
    definition: dict[str, Any] = Field(default_factory=lambda: {"steps": []})

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, definition: dict[str, Any]) -> dict[str, Any]:
        validate_definition(definition)
        return definition


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: str
    category: str
    definition: dict[str, Any]
    created_by: str
    created_at: datetime


class CredentialCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    secret: SecretStr = Field(min_length=1, max_length=8000)


class CredentialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    created_by: str
    created_at: datetime


class TenantPolicyUpdate(BaseModel):
    max_bots: int = Field(ge=0, le=500)
    max_concurrent_executions: int = Field(ge=1, le=100)
    max_executions_per_day: int = Field(ge=1, le=100_000)


class TenantPolicyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: uuid.UUID
    max_bots: int
    max_concurrent_executions: int
    max_executions_per_day: int
    updated_by: str
    updated_at: datetime
