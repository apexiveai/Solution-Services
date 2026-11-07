import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RequestKind = Literal["SERVICE", "LICENSE", "RENEWAL"]
Deployment = Literal["AEOP_CLOUD", "PRIVATE_CLOUD", "ON_PREMISES", "HYBRID"]


class OpportunityCreate(BaseModel):
    request_kind: RequestKind
    service_type: str = Field(min_length=2, max_length=80)
    departments: list[str] = Field(default_factory=list, max_length=20)
    requested_developers: int = Field(default=1, ge=1, le=100_000)
    requested_bots: int = Field(default=1, ge=1, le=100_000)
    plan_code: str = Field(default="ENTERPRISE", min_length=2, max_length=60)
    deployment: Deployment = "AEOP_CLOUD"
    term_months: int = Field(default=12, ge=1, le=60)
    requirements: str = Field(default="", max_length=5000)
    renewal_license_id: uuid.UUID | None = None


class OpportunityPricing(BaseModel):
    status: Literal["ASSESSMENT", "POC", "QUOTED", "DECLINED", "COMPLETED"]
    quote_amount: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=2)
    currency: str = Field(default="MMK", min_length=3, max_length=3)
    quote_valid_until: datetime | None = None
    quote_notes: str | None = Field(default=None, max_length=5000)
    plan_code: str | None = Field(default=None, min_length=2, max_length=60)
    approved_developers: int | None = Field(default=None, ge=1, le=100_000)
    approved_bots: int | None = Field(default=None, ge=1, le=100_000)
    approved_monthly_executions: int | None = Field(default=None, ge=1, le=10_000_000)
    term_months: int | None = Field(default=None, ge=1, le=60)


class OpportunityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    request_kind: str
    service_type: str
    departments: list[str]
    requested_developers: int
    requested_bots: int
    plan_code: str
    approved_developers: int | None
    approved_bots: int | None
    approved_monthly_executions: int | None
    deployment: str
    term_months: int
    requirements: str
    renewal_license_id: uuid.UUID | None
    status: str
    quote_amount: Decimal | None
    currency: str
    quote_valid_until: datetime | None
    quote_notes: str | None
    requested_by: str
    created_at: datetime
    updated_at: datetime


class AgreementAcceptance(BaseModel):
    accepted: Literal[True]
    agreement_reference: str | None = Field(default=None, max_length=255)


class PaymentSubmission(BaseModel):
    payment_reference: str = Field(min_length=3, max_length=255)


class PaymentDecision(BaseModel):
    verified: bool
    notes: str | None = Field(default=None, max_length=2000)


class DeveloperSeatCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=255)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    opportunity_id: uuid.UUID
    order_number: str
    plan_code: str
    developer_limit: int
    bot_limit: int
    monthly_execution_limit: int
    deployment: str
    term_months: int
    amount: Decimal
    currency: str
    renewal_license_id: uuid.UUID | None
    agreement_accepted: bool
    agreement_reference: str | None
    agreement_accepted_by: str | None
    agreement_accepted_at: datetime | None
    payment_reference: str | None
    payment_verified_at: datetime | None
    payment_verified_by: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class LicenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    order_id: uuid.UUID
    plan_code: str
    developer_limit: int
    bot_limit: int
    monthly_execution_limit: int
    deployment: str
    starts_at: datetime
    expires_at: datetime
    status: str
    created_at: datetime
