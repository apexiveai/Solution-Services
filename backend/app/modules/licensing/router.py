from calendar import monthrange
import uuid
from datetime import datetime, timedelta, timezone
from secrets import token_hex

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.automation.dependencies import record_audit, require_automation_role
from app.modules.automation.models import AutomationBot, AutomationExecution
from app.modules.licensing.models import (
    CoreRpaDeveloperSeat,
    CoreRpaLicense,
    CoreRpaOpportunity,
    CoreRpaOrder,
)
from app.modules.licensing.schemas import (
    AgreementAcceptance,
    DeveloperSeatCreate,
    LicenseRead,
    OpportunityCreate,
    OpportunityPricing,
    OpportunityRead,
    OrderRead,
    PaymentDecision,
    PaymentSubmission,
)
from app.modules.licensing.service import (
    get_active_license,
    require_active_license,
    require_sales_role,
    tenant_uuid,
)
from app.security import CurrentPrincipal, get_current_principal

router = APIRouter(prefix="/api/v1/core-rpa", tags=["Apexive CoreRPA Licensing"])
SERVICE_TYPES = {
    "ENTERPRISE_PROCESS_ASSESSMENT",
    "PROOF_OF_CONCEPT",
    "ENTERPRISE_QUOTATION",
    "LICENSING_DEPLOYMENT",
    "CUSTOM_BOT_DEVELOPMENT",
    "TRAINING_ANNUAL_SUPPORT",
}


def _add_months(value: datetime, months: int) -> datetime:
    month_index = value.year * 12 + value.month - 1 + months
    year, month = divmod(month_index, 12)
    month += 1
    return value.replace(
        year=year,
        month=month,
        day=min(value.day, monthrange(year, month)[1]),
    )


def _opportunity(
    db: Session,
    opportunity_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> CoreRpaOpportunity:
    record = db.scalar(
        select(CoreRpaOpportunity).where(
            CoreRpaOpportunity.id == opportunity_id,
            CoreRpaOpportunity.tenant_id == tenant_id,
        )
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Sales opportunity not found")
    return record


def _order(db: Session, order_id: uuid.UUID, tenant_id: uuid.UUID) -> CoreRpaOrder:
    record = db.scalar(
        select(CoreRpaOrder).where(
            CoreRpaOrder.id == order_id,
            CoreRpaOrder.tenant_id == tenant_id,
        )
    )
    if record is None:
        raise HTTPException(status_code=404, detail="CoreRPA order not found")
    return record


def _sales_opportunity(db: Session, opportunity_id: uuid.UUID) -> CoreRpaOpportunity:
    record = db.get(CoreRpaOpportunity, opportunity_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Sales opportunity not found")
    return record


def _sales_order(db: Session, order_id: uuid.UUID) -> CoreRpaOrder:
    record = db.get(CoreRpaOrder, order_id)
    if record is None:
        raise HTTPException(status_code=404, detail="CoreRPA order not found")
    return record


@router.post("/opportunities", response_model=OpportunityRead, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOpportunity:
    if payload.request_kind == "SERVICE" and payload.service_type not in SERVICE_TYPES:
        raise HTTPException(status_code=422, detail="Select a supported ApexiveAI service")
    if payload.request_kind == "RENEWAL" and payload.renewal_license_id is None:
        raise HTTPException(status_code=422, detail="A license is required for a renewal request")
    if payload.request_kind != "RENEWAL" and payload.renewal_license_id is not None:
        raise HTTPException(status_code=422, detail="Only renewal requests may reference a license")

    tenant_id = tenant_uuid(principal)
    if payload.renewal_license_id:
        renewal_license = db.scalar(
            select(CoreRpaLicense).where(
                CoreRpaLicense.id == payload.renewal_license_id,
                CoreRpaLicense.tenant_id == tenant_id,
            )
        )
        if renewal_license is None:
            raise HTTPException(status_code=404, detail="CoreRPA license not found")
    opportunity = CoreRpaOpportunity(
        tenant_id=tenant_id,
        request_kind=payload.request_kind,
        service_type=payload.service_type,
        departments=[department.strip() for department in payload.departments],
        requested_developers=payload.requested_developers,
        requested_bots=payload.requested_bots,
        plan_code=payload.plan_code.strip().upper(),
        deployment=payload.deployment,
        term_months=payload.term_months,
        requirements=payload.requirements.strip(),
        renewal_license_id=payload.renewal_license_id,
        requested_by=principal.subject,
    )
    db.add(opportunity)
    db.flush()
    db.add(record_audit(tenant_id, principal, "core_rpa.opportunity_created", "opportunity", opportunity.id))
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.get("/opportunities", response_model=list[OpportunityRead])
def list_opportunities(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[CoreRpaOpportunity]:
    statement = select(CoreRpaOpportunity)
    if not {"sales", "sales_admin", "platform_admin", "system_admin", "super_admin"}.intersection(
        role.casefold() for role in principal.roles
    ):
        statement = statement.where(CoreRpaOpportunity.tenant_id == tenant_uuid(principal))
    return list(
        db.scalars(statement.order_by(CoreRpaOpportunity.created_at.desc()).offset(offset).limit(limit))
    )


@router.patch("/opportunities/{opportunity_id}/quotation", response_model=OpportunityRead)
def update_quotation(
    opportunity_id: uuid.UUID,
    payload: OpportunityPricing,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOpportunity:
    require_sales_role(principal)
    opportunity = _sales_opportunity(db, opportunity_id)
    if opportunity.status in {"ACCEPTED", "DECLINED", "COMPLETED"}:
        raise HTTPException(status_code=409, detail="This sales opportunity is already closed")
    if payload.status == "QUOTED":
        if payload.quote_amount is None:
            raise HTTPException(status_code=422, detail="A price is required before issuing a quotation")
        if payload.quote_valid_until is None or payload.quote_valid_until <= datetime.now(timezone.utc):
            raise HTTPException(status_code=422, detail="Quotation expiry must be in the future")
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None or field in {"quote_amount", "quote_valid_until", "quote_notes"}:
            setattr(opportunity, field, value)
    opportunity.currency = payload.currency.upper()
    db.add(
        record_audit(
            opportunity.tenant_id,
            principal,
            f"core_rpa.opportunity_{payload.status.lower()}",
            "opportunity",
            opportunity.id,
        )
    )
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.post(
    "/opportunities/{opportunity_id}/orders",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def place_order(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOrder:
    tenant_id = tenant_uuid(principal)
    opportunity = _opportunity(db, opportunity_id, tenant_id)
    if opportunity.request_kind not in {"LICENSE", "RENEWAL"}:
        raise HTTPException(status_code=409, detail="Only CoreRPA license quotations can become software orders")
    if opportunity.status != "QUOTED" or opportunity.quote_amount is None:
        raise HTTPException(status_code=409, detail="The quotation must be issued before ordering")
    now = datetime.now(timezone.utc)
    if opportunity.quote_valid_until and opportunity.quote_valid_until <= now:
        raise HTTPException(status_code=409, detail="This quotation has expired")
    if opportunity.renewal_license_id is not None:
        duplicate = db.scalar(
            select(CoreRpaOrder.id).where(
                CoreRpaOrder.opportunity_id == opportunity.id,
                CoreRpaOrder.status != "CANCELLED",
            )
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="An order already exists for this quotation")

    order = CoreRpaOrder(
        tenant_id=tenant_id,
        opportunity_id=opportunity.id,
        order_number=f"CRPA-{now:%Y%m%d}-{token_hex(4).upper()}",
        plan_code=opportunity.plan_code,
        developer_limit=opportunity.approved_developers or opportunity.requested_developers,
        bot_limit=opportunity.approved_bots or opportunity.requested_bots,
        monthly_execution_limit=opportunity.approved_monthly_executions or 1000,
        deployment=opportunity.deployment,
        term_months=opportunity.term_months,
        amount=opportunity.quote_amount,
        currency=opportunity.currency,
        renewal_license_id=opportunity.renewal_license_id,
    )
    opportunity.status = "ACCEPTED"
    db.add(order)
    db.flush()
    db.add(record_audit(tenant_id, principal, "core_rpa.order_placed", "order", order.id))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Could not create a unique CoreRPA order") from exc
    db.refresh(order)
    return order


@router.get("/orders", response_model=list[OrderRead])
def list_orders(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[CoreRpaOrder]:
    statement = select(CoreRpaOrder)
    if not {"sales", "sales_admin", "platform_admin", "system_admin", "super_admin"}.intersection(
        role.casefold() for role in principal.roles
    ):
        statement = statement.where(CoreRpaOrder.tenant_id == tenant_uuid(principal))
    return list(db.scalars(statement.order_by(CoreRpaOrder.created_at.desc()).offset(offset).limit(limit)))


@router.post("/orders/{order_id}/agreement", response_model=OrderRead)
def accept_agreement(
    order_id: uuid.UUID,
    payload: AgreementAcceptance,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOrder:
    tenant_id = tenant_uuid(principal)
    order = _order(db, order_id, tenant_id)
    if order.status != "AGREEMENT_REQUIRED":
        raise HTTPException(status_code=409, detail="The order is not awaiting an agreement")
    order.agreement_accepted = True
    order.agreement_reference = payload.agreement_reference
    order.agreement_accepted_by = principal.subject
    order.agreement_accepted_at = datetime.now(timezone.utc)
    order.status = "PAYMENT_DUE"
    db.add(record_audit(tenant_id, principal, "core_rpa.agreement_accepted", "order", order.id))
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/payment", response_model=OrderRead)
def submit_payment_reference(
    order_id: uuid.UUID,
    payload: PaymentSubmission,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOrder:
    tenant_id = tenant_uuid(principal)
    order = _order(db, order_id, tenant_id)
    if order.status != "PAYMENT_DUE" or not order.agreement_accepted:
        raise HTTPException(status_code=409, detail="Accept the license agreement before submitting payment")
    order.payment_reference = payload.payment_reference.strip()
    order.status = "PAYMENT_REVIEW"
    db.add(record_audit(tenant_id, principal, "core_rpa.payment_submitted", "order", order.id))
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/payment-decision", response_model=OrderRead)
def decide_payment(
    order_id: uuid.UUID,
    payload: PaymentDecision,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOrder:
    require_sales_role(principal)
    order = _sales_order(db, order_id)
    if order.status != "PAYMENT_REVIEW":
        raise HTTPException(status_code=409, detail="The order has no payment awaiting verification")
    if not payload.verified:
        order.status = "PAYMENT_DUE"
        db.add(
            record_audit(
                order.tenant_id,
                principal,
                "core_rpa.payment_rejected",
                "order",
                order.id,
                {"notes": payload.notes or ""},
            )
        )
        db.commit()
        db.refresh(order)
        return order

    if not order.agreement_accepted or not order.payment_reference:
        raise HTTPException(status_code=409, detail="Agreement and payment reference are required")
    now = datetime.now(timezone.utc)
    order.payment_verified_at = now
    order.payment_verified_by = principal.subject
    order.status = "ACTIVE"
    license_record = None
    if order.renewal_license_id:
        license_record = db.scalar(
            select(CoreRpaLicense).where(
                CoreRpaLicense.id == order.renewal_license_id,
                CoreRpaLicense.tenant_id == order.tenant_id,
            )
        )
        if license_record is None:
            raise HTTPException(status_code=404, detail="Renewal license not found")
        starts_at = max(license_record.expires_at, now)
        license_record.expires_at = _add_months(starts_at, order.term_months)
        license_record.starts_at = min(license_record.starts_at, now)
        license_record.status = "ACTIVE"
        license_record.plan_code = order.plan_code
        license_record.developer_limit = order.developer_limit
        license_record.bot_limit = order.bot_limit
        license_record.monthly_execution_limit = order.monthly_execution_limit
        license_record.deployment = order.deployment
        license_record.order_id = order.id
    else:
        license_record = CoreRpaLicense(
            tenant_id=order.tenant_id,
            order_id=order.id,
            plan_code=order.plan_code,
            developer_limit=order.developer_limit,
            bot_limit=order.bot_limit,
            monthly_execution_limit=order.monthly_execution_limit,
            deployment=order.deployment,
            starts_at=now,
            expires_at=_add_months(now, order.term_months),
            status="ACTIVE",
        )
        db.add(license_record)
    db.flush()
    db.add(
        record_audit(
            order.tenant_id,
            principal,
            "core_rpa.license_activated",
            "license",
            license_record.id if license_record.id else order.id,
            {"order_number": order.order_number, "notes": payload.notes or ""},
        )
    )
    db.commit()
    db.refresh(order)
    return order


@router.get("/licenses", response_model=list[LicenseRead])
def list_licenses(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[CoreRpaLicense]:
    return list(
        db.scalars(
            select(CoreRpaLicense)
            .where(CoreRpaLicense.tenant_id == tenant_uuid(principal))
            .order_by(CoreRpaLicense.expires_at.desc())
        )
    )


@router.post(
    "/licenses/{license_id}/renewal",
    response_model=OpportunityRead,
    status_code=status.HTTP_201_CREATED,
)
def request_renewal(
    license_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> CoreRpaOpportunity:
    tenant_id = tenant_uuid(principal)
    license_record = db.scalar(
        select(CoreRpaLicense).where(
            CoreRpaLicense.id == license_id,
            CoreRpaLicense.tenant_id == tenant_id,
        )
    )
    if license_record is None:
        raise HTTPException(status_code=404, detail="CoreRPA license not found")
    opportunity = CoreRpaOpportunity(
        tenant_id=tenant_id,
        request_kind="RENEWAL",
        service_type="CORE_RPA_LICENSE_RENEWAL",
        departments=[],
        requested_developers=license_record.developer_limit,
        requested_bots=license_record.bot_limit,
        plan_code=license_record.plan_code,
        deployment=license_record.deployment,
        term_months=12,
        requirements="Customer-requested renewal.",
        renewal_license_id=license_record.id,
        requested_by=principal.subject,
    )
    db.add(opportunity)
    db.flush()
    db.add(record_audit(tenant_id, principal, "core_rpa.renewal_requested", "opportunity", opportunity.id))
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.get("/renewals/due")
def list_renewals_due(
    within_days: int = Query(default=30, ge=1, le=180),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[dict]:
    require_sales_role(principal)
    due_by = datetime.now(timezone.utc) + timedelta(days=within_days)
    records = db.scalars(
        select(CoreRpaLicense)
        .where(
            CoreRpaLicense.status == "ACTIVE",
            CoreRpaLicense.expires_at <= due_by,
        )
        .order_by(CoreRpaLicense.expires_at)
    )
    return [
        {
            "license_id": str(record.id),
            "plan_code": record.plan_code,
            "expires_at": record.expires_at,
            "days_remaining": max(0, (record.expires_at - datetime.now(timezone.utc)).days),
        }
        for record in records
    ]


@router.post("/renewals/prepare", response_model=list[OpportunityRead])
def prepare_renewal_quotations(
    within_days: int = Query(default=30, ge=1, le=180),
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[CoreRpaOpportunity]:
    require_sales_role(principal)
    now = datetime.now(timezone.utc)
    renewal_licenses = list(
        db.scalars(
            select(CoreRpaLicense).where(
                CoreRpaLicense.status == "ACTIVE",
                CoreRpaLicense.expires_at <= now + timedelta(days=within_days),
            )
        )
    )
    prepared = []
    for license_record in renewal_licenses:
        open_renewal = db.scalar(
            select(CoreRpaOpportunity.id).where(
                CoreRpaOpportunity.renewal_license_id == license_record.id,
                CoreRpaOpportunity.status.in_(("SUBMITTED", "ASSESSMENT", "POC", "QUOTED")),
            )
        )
        if open_renewal:
            continue
        prior_order = db.scalar(
            select(CoreRpaOrder)
            .where(
                CoreRpaOrder.id == license_record.order_id,
                CoreRpaOrder.tenant_id == license_record.tenant_id,
                CoreRpaOrder.status == "ACTIVE",
            )
        )
        opportunity = CoreRpaOpportunity(
            tenant_id=license_record.tenant_id,
            request_kind="RENEWAL",
            service_type="CORE_RPA_LICENSE_RENEWAL",
            departments=[],
            requested_developers=license_record.developer_limit,
            requested_bots=license_record.bot_limit,
            plan_code=license_record.plan_code,
            deployment=license_record.deployment,
            term_months=12,
            requirements="Renewal quotation prepared from current license entitlements.",
            renewal_license_id=license_record.id,
            status="QUOTED" if prior_order else "ASSESSMENT",
            quote_amount=prior_order.amount if prior_order else None,
            currency=prior_order.currency if prior_order else "MMK",
            quote_valid_until=now + timedelta(days=30) if prior_order else None,
            quote_notes=(
                "Renewal pricing is based on the previous order; review before sharing."
                if prior_order
                else "Set renewal pricing before sending this quotation."
            ),
            approved_developers=license_record.developer_limit,
            approved_bots=license_record.bot_limit,
            approved_monthly_executions=license_record.monthly_execution_limit,
            requested_by=principal.subject,
        )
        db.add(opportunity)
        db.flush()
        prepared.append(opportunity)
        db.add(
            record_audit(
                license_record.tenant_id,
                principal,
                "core_rpa.renewal_quote_prepared",
                "opportunity",
                opportunity.id,
            )
        )
    db.commit()
    for opportunity in prepared:
        db.refresh(opportunity)
    return prepared


@router.get("/usage")
def get_license_usage(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    tenant_id = tenant_uuid(principal)
    license_record = get_active_license(db, tenant_id)
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    bots = db.scalar(
        select(func.count(AutomationBot.id)).where(AutomationBot.tenant_id == tenant_id)
    ) or 0
    executions = db.scalar(
        select(func.count(AutomationExecution.id)).where(
            AutomationExecution.tenant_id == tenant_id,
            AutomationExecution.created_at >= month_start,
        )
    ) or 0
    developer_seats = db.scalar(
        select(func.count(CoreRpaDeveloperSeat.id)).where(
            CoreRpaDeveloperSeat.tenant_id == tenant_id
        )
    ) or 0
    return {
        "license": LicenseRead.model_validate(license_record).model_dump(mode="json")
        if license_record
        else None,
        "bots_used": bots,
        "bots_limit": license_record.bot_limit if license_record else 0,
        "executions_this_month": executions,
        "executions_limit": license_record.monthly_execution_limit if license_record else 0,
        "developers_limit": license_record.developer_limit if license_record else 0,
        "developers_used": developer_seats,
        "compliant": bool(license_record)
        and bots <= license_record.bot_limit
        and executions <= license_record.monthly_execution_limit
        and developer_seats <= license_record.developer_limit,
        "renewal_due": bool(license_record and license_record.expires_at <= now + timedelta(days=30)),
    }


@router.get("/developers")
def list_developer_seats(
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> list[dict]:
    tenant_id = tenant_uuid(principal)
    seats = db.scalars(
        select(CoreRpaDeveloperSeat)
        .where(CoreRpaDeveloperSeat.tenant_id == tenant_id)
        .order_by(CoreRpaDeveloperSeat.created_at)
    )
    return [
        {
            "id": str(seat.id),
            "subject": seat.subject,
            "assigned_by": seat.assigned_by,
            "created_at": seat.created_at,
        }
        for seat in seats
    ]


@router.post("/developers", status_code=status.HTTP_201_CREATED)
def assign_developer_seat(
    payload: DeveloperSeatCreate,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> dict:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    license_record = require_active_license(db, tenant_id)
    existing = db.scalar(
        select(CoreRpaDeveloperSeat).where(
            CoreRpaDeveloperSeat.tenant_id == tenant_id,
            CoreRpaDeveloperSeat.subject == payload.subject.strip(),
        )
    )
    if existing:
        raise HTTPException(status_code=409, detail="This user already has a developer seat")
    seat_count = db.scalar(
        select(func.count(CoreRpaDeveloperSeat.id)).where(
            CoreRpaDeveloperSeat.tenant_id == tenant_id
        )
    ) or 0
    if seat_count >= license_record.developer_limit:
        raise HTTPException(status_code=429, detail="Licensed CoreRPA developer limit reached")
    seat = CoreRpaDeveloperSeat(
        tenant_id=tenant_id,
        subject=payload.subject.strip(),
        assigned_by=principal.subject,
    )
    db.add(seat)
    db.flush()
    db.add(record_audit(tenant_id, principal, "core_rpa.developer_seat_assigned", "developer_seat", seat.id))
    db.commit()
    return {"id": str(seat.id), "subject": seat.subject, "assigned_by": seat.assigned_by}


@router.delete("/developers/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_developer_seat(
    seat_id: uuid.UUID,
    db: Session = Depends(get_db),
    principal: CurrentPrincipal = Depends(get_current_principal),
) -> None:
    require_automation_role(principal, "admin")
    tenant_id = tenant_uuid(principal)
    seat = db.scalar(
        select(CoreRpaDeveloperSeat).where(
            CoreRpaDeveloperSeat.id == seat_id,
            CoreRpaDeveloperSeat.tenant_id == tenant_id,
        )
    )
    if seat is None:
        raise HTTPException(status_code=404, detail="Developer seat not found")
    db.add(record_audit(tenant_id, principal, "core_rpa.developer_seat_revoked", "developer_seat", seat.id))
    db.delete(seat)
    db.commit()
