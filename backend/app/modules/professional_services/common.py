import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, ValidationError, create_model
from sqlalchemy import DateTime, ForeignKey, JSON, String, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base, get_db
from app.security import CurrentPrincipal, get_current_principal


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ProfessionalServicesTenantMixin:
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ProfessionalServicesTimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


class ProfessionalServicesRecordMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="PLANNED",
        index=True,
    )
    details: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )


def tenant_uuid(principal: CurrentPrincipal) -> uuid.UUID:
    try:
        return uuid.UUID(principal.tenant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token contains an invalid tenant_id claim",
        ) from exc


def register_resource_routes(
    router: APIRouter,
    resource_path: str,
    model: type[Base],
    create_schema: type[BaseModel],
    read_schema: type[BaseModel],
    *,
    references: dict[str, Any] | None = None,
) -> None:
    resource_name = resource_path.replace("-", " ").replace("/", " ").strip()
    update_schema = create_model(
        f"{create_schema.__name__}Update",
        __config__=ConfigDict(extra="forbid"),
        **{
            field_name: (field.annotation | None, None)
            for field_name, field in create_schema.model_fields.items()
        },
    )

    def verify_references(values: dict[str, Any], tenant_id: uuid.UUID, db: Session) -> None:
        for field_name, reference in (references or {}).items():
            referenced_id = values.get(field_name)
            if referenced_id is None:
                continue
            referenced_model = reference[0] if isinstance(reference, tuple) else reference
            related_field = reference[1] if isinstance(reference, tuple) else None
            related_value_field = reference[2] if isinstance(reference, tuple) else None
            conditions = [
                referenced_model.id == referenced_id,
                referenced_model.tenant_id == tenant_id,
            ]
            if related_field is not None and related_value_field is not None:
                conditions.append(
                    getattr(referenced_model, related_field)
                    == values.get(related_value_field)
                )
            exists = db.scalar(
                select(referenced_model.id).where(*conditions)
            )
            if exists is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"{field_name} must reference a record in this tenant",
                )

    def create_resource(
        payload: Any,
        db: Session = Depends(get_db),
        principal: CurrentPrincipal = Depends(get_current_principal),
    ) -> Any:
        tenant_id = tenant_uuid(principal)
        values = payload.model_dump()
        verify_references(values, tenant_id, db)
        record = model(tenant_id=tenant_id, **values)
        db.add(record)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{resource_name} conflicts with an existing record",
            ) from exc
        db.refresh(record)
        return record

    def list_resources(
        limit: int = Query(default=100, ge=1, le=200),
        offset: int = Query(default=0, ge=0),
        db: Session = Depends(get_db),
        principal: CurrentPrincipal = Depends(get_current_principal),
    ) -> list[Any]:
        tenant_id = tenant_uuid(principal)
        return list(
            db.scalars(
                select(model)
                .where(model.tenant_id == tenant_id)
                .order_by(model.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )

    def get_resource(
        resource_id: uuid.UUID,
        db: Session = Depends(get_db),
        principal: CurrentPrincipal = Depends(get_current_principal),
    ) -> Any:
        tenant_id = tenant_uuid(principal)
        record = db.scalar(
            select(model).where(
                model.id == resource_id,
                model.tenant_id == tenant_id,
            )
        )
        if record is None:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        return record

    def update_resource(
        resource_id: uuid.UUID,
        payload: Any,
        db: Session = Depends(get_db),
        principal: CurrentPrincipal = Depends(get_current_principal),
    ) -> Any:
        tenant_id = tenant_uuid(principal)
        record = db.scalar(
            select(model).where(
                model.id == resource_id,
                model.tenant_id == tenant_id,
            )
        )
        if record is None:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        changes = payload.model_dump(exclude_unset=True)
        if not changes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="At least one field must be provided",
            )
        values = {
            field_name: getattr(record, field_name)
            for field_name in create_schema.model_fields
        }
        try:
            validated = create_schema.model_validate({**values, **changes}).model_dump()
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=exc.errors(include_url=False),
            ) from exc
        verify_references(validated, tenant_id, db)
        for field_name in changes:
            setattr(record, field_name, validated[field_name])
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"{resource_name} conflicts with an existing record",
            ) from exc
        db.refresh(record)
        return record

    def add_route(
        endpoint: Callable[..., Any],
        *,
        path: str,
        methods: list[str],
        response_model: Any,
        status_code: int = status.HTTP_200_OK,
        name: str,
    ) -> None:
        router.add_api_route(
            path,
            endpoint,
            methods=methods,
            response_model=response_model,
            status_code=status_code,
            name=name,
        )

    create_resource.__annotations__["payload"] = create_schema
    list_resources.__annotations__["return"] = list[read_schema]
    get_resource.__annotations__["return"] = read_schema
    update_resource.__annotations__["payload"] = update_schema
    update_resource.__annotations__["return"] = read_schema

    add_route(
        create_resource,
        path=f"/{resource_path}",
        methods=["POST"],
        response_model=read_schema,
        status_code=status.HTTP_201_CREATED,
        name=f"create_{resource_path.replace('-', '_')}",
    )
    add_route(
        list_resources,
        path=f"/{resource_path}",
        methods=["GET"],
        response_model=list[read_schema],
        name=f"list_{resource_path.replace('-', '_')}",
    )
    add_route(
        get_resource,
        path=f"/{resource_path}/{{resource_id}}",
        methods=["GET"],
        response_model=read_schema,
        name=f"get_{resource_path.replace('-', '_')}",
    )
    add_route(
        update_resource,
        path=f"/{resource_path}/{{resource_id}}",
        methods=["PATCH"],
        response_model=read_schema,
        name=f"update_{resource_path.replace('-', '_')}",
    )


def register_overview_route(
    router: APIRouter,
    resources: dict[str, type[Base]],
) -> None:
    def get_overview(
        db: Session = Depends(get_db),
        principal: CurrentPrincipal = Depends(get_current_principal),
    ) -> dict[str, int]:
        tenant_id = tenant_uuid(principal)
        return {
            resource_name: db.scalar(
                select(func.count()).select_from(model).where(model.tenant_id == tenant_id)
            )
            or 0
            for resource_name, model in resources.items()
        }

    router.add_api_route(
        "/overview",
        get_overview,
        methods=["GET"],
        response_model=dict[str, int],
        name="get_overview",
    )
