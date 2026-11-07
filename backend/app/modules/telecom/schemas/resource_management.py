from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# =========================
# SITE SCHEMAS
# =========================

class SiteCreate(BaseModel):
    site_code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=200)
    site_type: str = Field(min_length=1, max_length=40)
    status: str = "ACTIVE"

    address: str | None = None
    city: str | None = Field(default=None, max_length=100)
    region: str | None = Field(default=None, max_length=100)
    country_code: str | None = Field(default=None, max_length=3)

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    elevation_meters: float | None = None

    metadata_json: dict = Field(default_factory=dict)


class SiteUpdate(BaseModel):
    site_code: str | None = Field(default=None, min_length=1, max_length=80)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    site_type: str | None = None
    status: str | None = None
    address: str | None = None
    city: str | None = None
    region: str | None = None
    country_code: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    elevation_meters: float | None = None
    metadata_json: dict | None = None


class SiteResponse(ORMBase):
    id: UUID
    tenant_id: UUID
    site_code: str
    name: str
    site_type: str
    status: str
    address: str | None
    city: str | None
    region: str | None
    country_code: str | None
    latitude: float | None
    longitude: float | None
    elevation_meters: float | None
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


# =========================
# DEVICE SCHEMAS
# =========================

class DeviceCreate(BaseModel):
    site_id: UUID | None = None
    device_code: str = Field(min_length=1, max_length=100)
    hostname: str = Field(min_length=1, max_length=200)
    device_type: str = Field(min_length=1, max_length=50)

    vendor: str | None = None
    model: str | None = None
    serial_number: str | None = None
    management_ip: str | None = None
    management_port: int | None = Field(default=None, ge=1, le=65535)

    status: str = "UNKNOWN"
    monitoring_enabled: bool = True
    metadata_json: dict = Field(default_factory=dict)


class DeviceUpdate(BaseModel):
    site_id: UUID | None = None
    device_code: str | None = None
    hostname: str | None = None
    device_type: str | None = None
    vendor: str | None = None
    model: str | None = None
    serial_number: str | None = None
    management_ip: str | None = None
    management_port: int | None = Field(default=None, ge=1, le=65535)
    status: str | None = None
    monitoring_enabled: bool | None = None
    metadata_json: dict | None = None


class DeviceResponse(ORMBase):
    id: UUID
    tenant_id: UUID
    site_id: UUID | None
    device_code: str
    hostname: str
    device_type: str
    vendor: str | None
    model: str | None
    serial_number: str | None
    management_ip: str | None
    management_port: int | None
    status: str
    monitoring_enabled: bool
    metadata_json: dict
    created_at: datetime
    updated_at: datetime


# =========================
# INTERFACE SCHEMAS
# =========================

class InterfaceCreate(BaseModel):
    device_id: UUID
    interface_name: str = Field(min_length=1, max_length=120)
    interface_type: str | None = None
    description: str | None = None
    mac_address: str | None = None
    ip_address: str | None = None
    speed_mbps: int | None = Field(default=None, ge=0)
    admin_status: str = "UNKNOWN"
    operational_status: str = "UNKNOWN"
    enabled: bool = True


class InterfaceUpdate(BaseModel):
    interface_name: str | None = None
    interface_type: str | None = None
    description: str | None = None
    mac_address: str | None = None
    ip_address: str | None = None
    speed_mbps: int | None = Field(default=None, ge=0)
    admin_status: str | None = None
    operational_status: str | None = None
    enabled: bool | None = None


class InterfaceResponse(ORMBase):
    id: UUID
    tenant_id: UUID
    device_id: UUID
    interface_name: str
    interface_type: str | None
    description: str | None
    mac_address: str | None
    ip_address: str | None
    speed_mbps: int | None
    admin_status: str
    operational_status: str
    enabled: bool
    created_at: datetime
    updated_at: datetime


# =========================
# CONNECTION SCHEMAS
# =========================

class ConnectionCreate(BaseModel):
    source_device_id: UUID
    target_device_id: UUID
    source_interface_id: UUID | None = None
    target_interface_id: UUID | None = None
    connection_type: str = "PHYSICAL"
    status: str = "UNKNOWN"
    bandwidth_mbps: int | None = Field(default=None, ge=0)
    description: str | None = None


class ConnectionUpdate(BaseModel):
    source_interface_id: UUID | None = None
    target_interface_id: UUID | None = None
    connection_type: str | None = None
    status: str | None = None
    bandwidth_mbps: int | None = Field(default=None, ge=0)
    description: str | None = None


class ConnectionResponse(ORMBase):
    id: UUID
    tenant_id: UUID
    source_device_id: UUID
    target_device_id: UUID
    source_interface_id: UUID | None
    target_interface_id: UUID | None
    connection_type: str
    status: str
    bandwidth_mbps: int | None
    description: str | None
    created_at: datetime
    updated_at: datetime