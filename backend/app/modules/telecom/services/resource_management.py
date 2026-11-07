from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.telecom.models.network import (
    TelecomSite,
    TelecomDevice,
    TelecomInterface,
    TelecomConnection,
)


def parse_tenant_id(value: str) -> UUID:
    try:
        return UUID(value)
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid tenant identity",
        )


def get_site(db: Session, tenant_id: UUID, site_id: UUID):
    item = db.query(TelecomSite).filter(
        TelecomSite.id == site_id,
        TelecomSite.tenant_id == tenant_id,
    ).first()

    if item is None:
        raise HTTPException(404, "Site not found")

    return item


def get_device(db: Session, tenant_id: UUID, device_id: UUID):
    item = db.query(TelecomDevice).filter(
        TelecomDevice.id == device_id,
        TelecomDevice.tenant_id == tenant_id,
    ).first()

    if item is None:
        raise HTTPException(404, "Device not found")

    return item


def get_interface(db: Session, tenant_id: UUID, interface_id: UUID):
    item = db.query(TelecomInterface).filter(
        TelecomInterface.id == interface_id,
        TelecomInterface.tenant_id == tenant_id,
    ).first()

    if item is None:
        raise HTTPException(404, "Interface not found")

    return item


def get_connection(db: Session, tenant_id: UUID, connection_id: UUID):
    item = db.query(TelecomConnection).filter(
        TelecomConnection.id == connection_id,
        TelecomConnection.tenant_id == tenant_id,
    ).first()

    if item is None:
        raise HTTPException(404, "Connection not found")

    return item


def ensure_site(
    db: Session,
    tenant_id: UUID,
    site_id: UUID | None,
):
    if site_id is None:
        return None

    return get_site(db, tenant_id, site_id)


def ensure_device(
    db: Session,
    tenant_id: UUID,
    device_id: UUID,
):
    return get_device(db, tenant_id, device_id)


def ensure_interface(
    db: Session,
    tenant_id: UUID,
    interface_id: UUID | None,
):
    if interface_id is None:
        return None

    return get_interface(db, tenant_id, interface_id)


def ensure_interface_belongs_to_device(
    db: Session,
    tenant_id: UUID,
    interface_id: UUID | None,
    device_id: UUID,
):
    if interface_id is None:
        return None

    interface = get_interface(db, tenant_id, interface_id)

    if interface.device_id != device_id:
        raise HTTPException(
            status_code=422,
            detail="Interface does not belong to the specified device",
        )

    return interface


def commit_changes(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Database constraint conflict. Check duplicate codes and related resources.",
        )
    except Exception:
        db.rollback()
        raise