import unittest
import uuid
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.modules.licensing.router import _add_months
from app.modules.licensing.schemas import OpportunityCreate
from app.modules.licensing.service import (
    enforce_bot_entitlement,
    require_active_license,
    require_developer_seat,
    require_sales_role,
)


class CoreRpaLicensingTests(unittest.TestCase):
    def test_license_terms_add_calendar_months(self) -> None:
        start = datetime(2024, 1, 31, 12, 0, tzinfo=timezone.utc)
        self.assertEqual(_add_months(start, 1), datetime(2024, 2, 29, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(_add_months(start, 12), datetime(2025, 1, 31, 12, 0, tzinfo=timezone.utc))

    def test_service_opportunity_validates_request_fields(self) -> None:
        opportunity = OpportunityCreate(
            request_kind="SERVICE",
            service_type="ENTERPRISE_PROCESS_ASSESSMENT",
            departments=["Finance", "IT"],
            requested_developers=3,
            requested_bots=5,
        )
        self.assertEqual(opportunity.requested_bots, 5)

    def test_tenant_administrator_cannot_quote_or_verify_payments(self) -> None:
        with self.assertRaises(HTTPException) as raised:
            require_sales_role(Mock(roles=["admin"]))
        self.assertEqual(raised.exception.status_code, 403)

    def test_sales_role_can_manage_enterprise_quotes(self) -> None:
        require_sales_role(Mock(roles=["SALES_ADMIN"]))

    def test_workload_requires_active_license(self) -> None:
        db = Mock()
        db.scalar.return_value = None
        with self.assertRaises(HTTPException) as raised:
            require_active_license(db, uuid.uuid4())
        self.assertEqual(raised.exception.status_code, 402)

    def test_bot_limit_is_enforced_from_active_license(self) -> None:
        db = Mock()
        license_record = Mock(bot_limit=2)
        with patch(
            "app.modules.licensing.service.require_active_license",
            return_value=license_record,
        ):
            db.scalar.return_value = 2
            with self.assertRaises(HTTPException) as raised:
                enforce_bot_entitlement(db, uuid.uuid4())
        self.assertEqual(raised.exception.status_code, 429)

    def test_developer_requires_assigned_tenant_seat(self) -> None:
        db = Mock()
        db.scalar.return_value = None
        with self.assertRaises(HTTPException) as raised:
            require_developer_seat(db, uuid.uuid4(), "developer-subject", ["developer"])
        self.assertEqual(raised.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
