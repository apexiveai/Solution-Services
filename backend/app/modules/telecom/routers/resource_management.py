from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import CurrentPrincipal, get_current_principal

from app.modules.telecom.models.network import (
    TelecomSite,
    TelecomDevice,
    TelecomInterface,
    TelecomConnection,
    TelecomTopologyLink,
)

from app.modules.telecom.schemas.resource_management import (
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    InterfaceCreate,
    InterfaceUpdate,
    InterfaceResponse,
    ConnectionCreate,
    ConnectionUpdate,
    ConnectionResponse,
)

from app.modules.telecom.services.resource_management import (
    parse_tenant_id,
    get_site,
    get_device,
    get_interface,
    get_connection,
    ensure_site,
    ensure_device,
    ensure_interface_belongs_to_device,
    commit_changes,
)

router = APIRouter(tags=["ARM - Resource Management"])


def tenant_of(principal: CurrentPrincipal) -> UUID:
    return parse_tenant_id(principal.tenant_id)


def apply_pagination(query, limit: int, offset: int):
    return query.offset(offset).limit(limit).all()


# ============================================================
# OVERVIEW
# ============================================================

@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    def count(model):
        return db.query(func.count(model.id)).filter(
            model.tenant_id == tenant_id
        ).scalar() or 0

    def grouped_status(model):
        rows = db.query(
            model.status,
            func.count(model.id),
        ).filter(
            model.tenant_id == tenant_id
        ).group_by(model.status).all()

        return {
            str(key or "UNKNOWN"): value
            for key, value in rows
        }

    return {
        "product": "ApexiveAI Resource Management",
        "module": "ARM",
        "tenant_id": str(tenant_id),
        "resources": {
            "sites": count(TelecomSite),
            "devices": count(TelecomDevice),
            "interfaces": count(TelecomInterface),
            "connections": count(TelecomConnection),
            "topology_links": count(TelecomTopologyLink),
        },
        "device_status": grouped_status(TelecomDevice),
        "site_status": grouped_status(TelecomSite),
        "connection_status": grouped_status(TelecomConnection),
    }


# ============================================================
# SITES
# ============================================================

@router.post(
    "/sites",
    response_model=SiteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_site(
    payload: SiteCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    item = TelecomSite(
        tenant_id=tenant_id,
        **payload.model_dump(),
    )

    db.add(item)
    commit_changes(db)
    db.refresh(item)

    return item


@router.get("/sites", response_model=list[SiteResponse])
def list_sites(
    q: str | None = None,
    site_type: str | None = None,
    site_status: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    query = db.query(TelecomSite).filter(
        TelecomSite.tenant_id == tenant_id
    )

    if q:
        search = f"%{q.strip()}%"
        query = query.filter(or_(
            TelecomSite.site_code.ilike(search),
            TelecomSite.name.ilike(search),
            TelecomSite.city.ilike(search),
            TelecomSite.region.ilike(search),
        ))

    if site_type:
        query = query.filter(TelecomSite.site_type == site_type)

    if site_status:
        query = query.filter(TelecomSite.status == site_status)

    return query.order_by(TelecomSite.created_at.desc()).offset(
        offset
    ).limit(limit).all()


@router.get("/sites/{site_id}", response_model=SiteResponse)
def read_site(
    site_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    return get_site(db, tenant_of(principal), site_id)


@router.patch("/sites/{site_id}", response_model=SiteResponse)
def update_site(
    site_id: UUID,
    payload: SiteUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    item = get_site(db, tenant_of(principal), site_id)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    commit_changes(db)
    db.refresh(item)

    return item


@router.delete("/sites/{site_id}")
def delete_site(
    site_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)
    item = get_site(db, tenant_id, site_id)

    has_devices = db.query(TelecomDevice.id).filter(
        TelecomDevice.tenant_id == tenant_id,
        TelecomDevice.site_id == site_id,
    ).first()

    if has_devices:
        raise HTTPException(
            status_code=409,
            detail="Site cannot be deleted while devices are assigned to it",
        )

    db.delete(item)
    commit_changes(db)

    return {"deleted": True, "id": str(site_id)}


# ============================================================
# DEVICES
# ============================================================

@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    payload: DeviceCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    ensure_site(db, tenant_id, payload.site_id)

    item = TelecomDevice(
        tenant_id=tenant_id,
        **payload.model_dump(),
    )

    db.add(item)
    commit_changes(db)
    db.refresh(item)

    return item


@router.get("/devices", response_model=list[DeviceResponse])
def list_devices(
    q: str | None = None,
    device_type: str | None = None,
    device_status: str | None = Query(default=None, alias="status"),
    site_id: UUID | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    query = db.query(TelecomDevice).filter(
        TelecomDevice.tenant_id == tenant_id
    )

    if q:
        search = f"%{q.strip()}%"
        query = query.filter(or_(
            TelecomDevice.device_code.ilike(search),
            TelecomDevice.hostname.ilike(search),
            TelecomDevice.vendor.ilike(search),
            TelecomDevice.model.ilike(search),
            TelecomDevice.management_ip.ilike(search),
        ))

    if device_type:
        query = query.filter(TelecomDevice.device_type == device_type)

    if device_status:
        query = query.filter(TelecomDevice.status == device_status)

    if site_id:
        query = query.filter(TelecomDevice.site_id == site_id)

    return query.order_by(TelecomDevice.created_at.desc()).offset(
        offset
    ).limit(limit).all()


@router.get("/devices/{device_id}", response_model=DeviceResponse)
def read_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    return get_device(db, tenant_of(principal), device_id)


@router.patch("/devices/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: UUID,
    payload: DeviceUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)
    item = get_device(db, tenant_id, device_id)

    changes = payload.model_dump(exclude_unset=True)

    if "site_id" in changes:
        ensure_site(db, tenant_id, changes["site_id"])

    for key, value in changes.items():
        setattr(item, key, value)

    commit_changes(db)
    db.refresh(item)

    return item


@router.delete("/devices/{device_id}")
def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)
    item = get_device(db, tenant_id, device_id)

    has_connections = db.query(TelecomConnection.id).filter(
        TelecomConnection.tenant_id == tenant_id,
        or_(
            TelecomConnection.source_device_id == device_id,
            TelecomConnection.target_device_id == device_id,
        ),
    ).first()

    if has_connections:
        raise HTTPException(
            status_code=409,
            detail="Device cannot be deleted while connections exist",
        )

    db.delete(item)
    commit_changes(db)

    return {"deleted": True, "id": str(device_id)}


# ============================================================
# INTERFACES
# ============================================================

@router.post(
    "/interfaces",
    response_model=InterfaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interface(
    payload: InterfaceCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)
    ensure_device(db, tenant_id, payload.device_id)

    item = TelecomInterface(
        tenant_id=tenant_id,
        **payload.model_dump(),
    )

    db.add(item)
    commit_changes(db)
    db.refresh(item)

    return item


@router.get("/interfaces", response_model=list[InterfaceResponse])
def list_interfaces(
    q: str | None = None,
    device_id: UUID | None = None,
    interface_status: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    query = db.query(TelecomInterface).filter(
        TelecomInterface.tenant_id == tenant_id
    )

    if q:
        search = f"%{q.strip()}%"
        query = query.filter(or_(
            TelecomInterface.interface_name.ilike(search),
            TelecomInterface.ip_address.ilike(search),
            TelecomInterface.mac_address.ilike(search),
            TelecomInterface.description.ilike(search),
        ))

    if device_id:
        query = query.filter(TelecomInterface.device_id == device_id)

    if interface_status:
        query = query.filter(
            TelecomInterface.operational_status == interface_status
        )

    return query.order_by(TelecomInterface.created_at.desc()).offset(
        offset
    ).limit(limit).all()


@router.get("/interfaces/{interface_id}", response_model=InterfaceResponse)
def read_interface(
    interface_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    return get_interface(db, tenant_of(principal), interface_id)


@router.patch("/interfaces/{interface_id}", response_model=InterfaceResponse)
def update_interface(
    interface_id: UUID,
    payload: InterfaceUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    item = get_interface(db, tenant_of(principal), interface_id)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    commit_changes(db)
    db.refresh(item)

    return item


@router.delete("/interfaces/{interface_id}")
def delete_interface(
    interface_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    item = get_interface(db, tenant_of(principal), interface_id)

    db.delete(item)
    commit_changes(db)

    return {"deleted": True, "id": str(interface_id)}


# ============================================================
# CONNECTIONS
# ============================================================

@router.post(
    "/connections",
    response_model=ConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_connection(
    payload: ConnectionCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    if payload.source_device_id == payload.target_device_id:
        raise HTTPException(
            status_code=422,
            detail="Source and target devices must be different",
        )

    ensure_device(db, tenant_id, payload.source_device_id)
    ensure_device(db, tenant_id, payload.target_device_id)

    ensure_interface_belongs_to_device(
        db,
        tenant_id,
        payload.source_interface_id,
        payload.source_device_id,
    )

    ensure_interface_belongs_to_device(
        db,
        tenant_id,
        payload.target_interface_id,
        payload.target_device_id,
    )

    item = TelecomConnection(
        tenant_id=tenant_id,
        **payload.model_dump(),
    )

    db.add(item)
    commit_changes(db)
    db.refresh(item)

    return item


@router.get("/connections", response_model=list[ConnectionResponse])
def list_connections(
    connection_type: str | None = None,
    connection_status: str | None = Query(default=None, alias="status"),
    device_id: UUID | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    query = db.query(TelecomConnection).filter(
        TelecomConnection.tenant_id == tenant_id
    )

    if connection_type:
        query = query.filter(
            TelecomConnection.connection_type == connection_type
        )

    if connection_status:
        query = query.filter(
            TelecomConnection.status == connection_status
        )

    if device_id:
        query = query.filter(or_(
            TelecomConnection.source_device_id == device_id,
            TelecomConnection.target_device_id == device_id,
        ))

    return query.order_by(TelecomConnection.created_at.desc()).offset(
        offset
    ).limit(limit).all()


@router.get("/connections/{connection_id}", response_model=ConnectionResponse)
def read_connection(
    connection_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    return get_connection(db, tenant_of(principal), connection_id)


@router.patch("/connections/{connection_id}", response_model=ConnectionResponse)
def update_connection(
    connection_id: UUID,
    payload: ConnectionUpdate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)
    item = get_connection(db, tenant_id, connection_id)

    changes = payload.model_dump(exclude_unset=True)

    ensure_interface_belongs_to_device(
        db,
        tenant_id,
        changes.get("source_interface_id", item.source_interface_id),
        item.source_device_id,
    )

    ensure_interface_belongs_to_device(
        db,
        tenant_id,
        changes.get("target_interface_id", item.target_interface_id),
        item.target_device_id,
    )

    for key, value in changes.items():
        setattr(item, key, value)

    commit_changes(db)
    db.refresh(item)

    return item


@router.delete("/connections/{connection_id}")
def delete_connection(
    connection_id: UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    item = get_connection(db, tenant_of(principal), connection_id)

    db.delete(item)
    commit_changes(db)

    return {"deleted": True, "id": str(connection_id)}


# ============================================================
# NETWORK TOPOLOGY
# ============================================================

@router.get("/topology")
def get_topology(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
):
    tenant_id = tenant_of(principal)

    devices = db.query(TelecomDevice).filter(
        TelecomDevice.tenant_id == tenant_id
    ).all()

    links = db.query(TelecomTopologyLink).filter(
        TelecomTopologyLink.tenant_id == tenant_id
    ).all()

    connections = db.query(TelecomConnection).filter(
        TelecomConnection.tenant_id == tenant_id
    ).all()

    return {
        "nodes": [
            {
                "id": str(device.id),
                "code": device.device_code,
                "label": device.hostname,
                "type": device.device_type,
                "status": device.status,
                "site_id": (
                    str(device.site_id)
                    if device.site_id else None
                ),
                "management_ip": device.management_ip,
            }
            for device in devices
        ],
        "links": [
            {
                "id": str(link.id),
                "source": str(link.source_device_id),
                "target": str(link.target_device_id),
                "connection_id": (
                    str(link.connection_id)
                    if link.connection_id else None
                ),
                "type": link.link_type,
                "status": link.status,
                "label": link.label,
            }
            for link in links
        ],
        "connections": [
            {
                "id": str(connection.id),
                "source": str(connection.source_device_id),
                "target": str(connection.target_device_id),
                "type": connection.connection_type,
                "status": connection.status,
                "bandwidth_mbps": connection.bandwidth_mbps,
            }
            for connection in connections
        ],
    }