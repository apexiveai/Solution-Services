import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FacilityCreate(BaseModel):
    facility_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    facility_type: str = Field(default="FACTORY", max_length=48)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    region: str | None = Field(default=None, max_length=100)
    address: str | None = None


class FacilityRead(FacilityCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime


class EquipmentCreate(BaseModel):
    equipment_code: str = Field(min_length=1, max_length=64)
    facility_code: str = Field(min_length=1, max_length=64)
    production_line: str | None = Field(default=None, max_length=96)
    name: str = Field(min_length=1, max_length=200)
    equipment_type: str = Field(min_length=1, max_length=64)
    manufacturer: str | None = Field(default=None, max_length=150)
    model_number: str | None = Field(default=None, max_length=100)
    criticality: str = Field(default="MEDIUM", max_length=24)


class EquipmentRead(EquipmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    rated_capacity: Decimal | None
    created_at: datetime
    updated_at: datetime


class DataSourceCreate(BaseModel):
    source_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    source_type: str = Field(min_length=1, max_length=48)
    protocol: str | None = Field(default=None, max_length=48)
    equipment_code: str | None = Field(default=None, max_length=64)


class DataSourceRead(DataSourceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    configuration: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class ProductionOrderCreate(BaseModel):
    order_number: str = Field(min_length=1, max_length=64)
    product_code: str = Field(min_length=1, max_length=64)
    product_name: str = Field(min_length=1, max_length=200)
    facility_code: str = Field(min_length=1, max_length=64)
    production_line: str | None = Field(default=None, max_length=96)
    planned_quantity: Decimal = Field(gt=0)
    unit_of_measure: str = Field(min_length=1, max_length=24)
    planned_start: datetime | None = None
    planned_end: datetime | None = None
    notes: str | None = None


class ProductionOrderRead(ProductionOrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    completed_quantity: Decimal
    status: str
    actual_start: datetime | None
    actual_end: datetime | None
    created_at: datetime
    updated_at: datetime


class MetricSampleCreate(BaseModel):
    source_code: str = Field(min_length=1, max_length=64)
    equipment_code: str | None = Field(default=None, max_length=64)
    metric_name: str = Field(min_length=1, max_length=96)
    value: Decimal
    unit: str | None = Field(default=None, max_length=32)
    observed_at: datetime
    dimensions: dict[str, Any] = Field(default_factory=dict)


class MetricSampleRead(MetricSampleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    quality_code: str
    created_at: datetime
