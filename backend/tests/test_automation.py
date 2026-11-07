import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import uuid

from fastapi import HTTPException
from pydantic import ValidationError

from app.config import settings
from app.modules.automation.crypto import decrypt_secret, encrypt_secret
from app.modules.automation.dependencies import require_automation_role
from app.modules.automation.integrations.api import (
    IntegrationTargetError,
    validate_api_target,
)
from app.modules.automation.integrations.files import resolve_workspace_file
from app.modules.automation.runtime.engine import (
    WorkflowExecutionError,
    WorkflowValidationError,
    execute_workflow,
    validate_definition,
    validate_steps,
)
from app.modules.automation.bots.router import (
    claim_studio_execution,
    complete_studio_execution,
)
from app.modules.automation.scheduler.service import next_schedule_run
from app.modules.automation.schemas import RuntimeCompletionCreate, WorkflowCreate
from app.security import CurrentPrincipal


class AutomationEngineTests(unittest.TestCase):
    def test_studio_runtimes_validate_separately_from_core_workflows(self) -> None:
        ais = WorkflowCreate(
            name="AIS workflow",
            definition={
                "runtime": "AIS",
                "contract_version": 1,
                "steps": [{"type": "prompt", "key": "summary", "prompt": "Summarize the input"}],
            },
        )
        cy = WorkflowCreate(
            name="CY policy",
            definition={
                "runtime": "CY",
                "contract_version": 1,
                "rules": [
                    {
                        "id": "failed-login",
                        "field": "event.type",
                        "equals": "failed_login",
                        "severity": "HIGH",
                        "title": "Failed login",
                        "recommended_response": "Review account activity",
                    }
                ],
            },
        )
        self.assertEqual(ais.definition["runtime"], "AIS")
        self.assertEqual(cy.definition["runtime"], "CY")

    def test_studio_runtimes_reject_unknown_or_unbounded_actions(self) -> None:
        with self.assertRaises(ValidationError):
            WorkflowCreate(
                name="AIS shell",
                definition={
                    "runtime": "AIS",
                    "contract_version": 1,
                    "steps": [{"type": "shell", "command": "not allowed"}],
                },
            )
        with self.assertRaises(ValidationError):
            WorkflowCreate(
                name="CY response",
                definition={
                    "runtime": "CY",
                    "contract_version": 1,
                    "rules": [
                        {
                            "id": "action",
                            "field": "event.type",
                            "equals": "alert",
                            "severity": "HIGH",
                            "title": "Alert",
                            "recommended_response": "run shell command",
                            "action": "execute",
                        }
                    ],
                },
            )

    def test_unversioned_core_workflow_contract_remains_valid(self) -> None:
        legacy = WorkflowCreate(
            name="Legacy Core workflow",
            definition={"steps": [{"type": "set_variable", "key": "state", "value": "ready"}]},
        )
        self.assertNotIn("runtime", legacy.definition)

    def test_runs_allowlisted_steps_and_returns_results(self) -> None:
        result = execute_workflow(
            {
                "steps": [
                    {"type": "set_variable", "key": "amount", "value": 2},
                    {
                        "type": "condition",
                        "variable": "amount",
                        "equals": 2,
                        "then": [{"type": "log", "message": "approved"}],
                    },
                    {
                        "type": "for_each",
                        "variable": "items",
                        "steps": [{"type": "set_variable", "key": "last", "value": "done"}],
                    },
                ]
            },
            {"items": [1, 2]},
        )

        self.assertEqual(result["variables"]["amount"], 2)
        self.assertEqual(result["variables"]["last"], "done")
        self.assertEqual(result["logs"], ["approved"])

    def test_rejects_external_actions_without_enabled_adapters(self) -> None:
        with self.assertRaises(WorkflowValidationError):
            validate_steps([{"type": "api_request", "url": "https://example.invalid"}])

    def test_for_each_has_a_hard_item_limit(self) -> None:
        with self.assertRaises(WorkflowExecutionError):
            execute_workflow(
                {"steps": [{"type": "for_each", "variable": "items", "steps": []}]},
                {"items": list(range(101))},
            )

    def test_while_and_parallel_steps_are_bounded_and_merge_results(self) -> None:
        result = execute_workflow(
            {
                "steps": [
                    {"type": "set_variable", "key": "continue", "value": True},
                    {
                        "type": "while",
                        "variable": "continue",
                        "equals": True,
                        "steps": [
                            {"type": "set_variable", "key": "continue", "value": False}
                        ],
                    },
                    {
                        "type": "parallel",
                        "branches": [
                            [{"type": "set_variable", "key": "left", "value": 1}],
                            [{"type": "set_variable", "key": "right", "value": 2}],
                        ],
                    },
                ]
            },
            {},
        )
        self.assertFalse(result["variables"]["continue"])
        self.assertEqual(result["variables"]["left"], 1)
        self.assertEqual(result["variables"]["right"], 2)

    def test_parallel_branches_cannot_write_conflicting_values(self) -> None:
        with self.assertRaises(WorkflowExecutionError):
            execute_workflow(
                {
                    "steps": [
                        {
                            "type": "parallel",
                            "branches": [
                                [{"type": "set_variable", "key": "result", "value": 1}],
                                [{"type": "set_variable", "key": "result", "value": 2}],
                            ],
                        }
                    ]
                },
                {},
            )

    def test_reusable_components_are_validated_and_executed(self) -> None:
        result = execute_workflow(
            {
                "steps": [{"type": "component", "name": "audit"}],
                "components": {
                    "audit": [{"type": "log", "message": "component ran"}]
                },
            },
            {},
        )
        self.assertEqual(result["logs"], ["component ran"])

    def test_recursive_components_are_rejected(self) -> None:
        with self.assertRaises(WorkflowValidationError):
            validate_definition(
                {
                    "steps": [{"type": "component", "name": "first"}],
                    "components": {
                        "first": [{"type": "component", "name": "second"}],
                        "second": [{"type": "component", "name": "first"}],
                    },
                }
            )

    def test_schema_rejects_unapproved_action_types(self) -> None:
        with self.assertRaises(ValidationError):
            WorkflowCreate(
                name="unsafe",
                definition={"steps": [{"type": "shell", "command": "echo unsafe"}]},
            )


class AutomationGovernanceTests(unittest.TestCase):
    def test_agent_service_role_is_limited_to_agent_operations(self) -> None:
        principal = CurrentPrincipal(
            subject="agent-client",
            tenant_id="c3b9c9b3-f53a-4416-b4c1-b88f36e045d2",
            roles=["core_rpa_agent"],
            claims={},
        )
        require_automation_role(principal, "agent")
        with self.assertRaises(HTTPException):
            require_automation_role(principal, "admin")

    def test_remote_execution_completion_requires_a_consistent_result(self) -> None:
        successful = RuntimeCompletionCreate(
            claim_attempt=1,
            status="SUCCEEDED",
            result_data={},
        )
        failed = RuntimeCompletionCreate(
            claim_attempt=1,
            status="FAILED",
            error_message="Model unavailable",
        )
        self.assertEqual(successful.status, "SUCCEEDED")
        self.assertEqual(failed.status, "FAILED")
        with self.assertRaises(ValidationError):
            RuntimeCompletionCreate(claim_attempt=1, status="SUCCEEDED")
        with self.assertRaises(ValidationError):
            RuntimeCompletionCreate(claim_attempt=1, status="FAILED")

    def test_credential_encryption_round_trips_with_configured_key(self) -> None:
        with patch.object(settings, "automation_credential_key", "test-key-" + "x" * 40):
            encrypted = encrypt_secret("private-value")
            self.assertNotEqual(encrypted, "private-value")
            self.assertEqual(decrypt_secret(encrypted), "private-value")

    def test_credential_encryption_requires_a_provisioned_key(self) -> None:
        with patch.object(settings, "automation_credential_key", ""):
            with self.assertRaisesRegex(RuntimeError, "must be configured"):
                encrypt_secret("private-value")

    def test_api_targets_require_https_and_exact_allowlisted_host(self) -> None:
        self.assertEqual(
            validate_api_target("https://api.example.com/v1", ["api.example.com"]),
            "api.example.com",
        )
        with self.assertRaises(IntegrationTargetError):
            validate_api_target("http://api.example.com", ["api.example.com"])
        with self.assertRaises(IntegrationTargetError):
            validate_api_target("https://not-approved.example", ["api.example.com"])

    def test_file_paths_cannot_escape_the_tenant_workspace(self) -> None:
        root = Path.cwd() / "workspace"
        with self.assertRaises(ValueError):
            resolve_workspace_file("../secret.txt", root)

    def test_schedule_calculates_next_run_in_requested_timezone(self) -> None:
        next_run = next_schedule_run(
            "0 9 * * *",
            "Asia/Yangon",
            datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(next_run.hour, 9)
        self.assertEqual(next_run.utcoffset().total_seconds(), 6.5 * 3600)

    def test_schedule_rejects_invalid_cron_expression(self) -> None:
        with self.assertRaises(HTTPException):
            next_schedule_run("not a cron expression")


class StudioAgentIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tenant_id = uuid.uuid4()
        self.bot_id = uuid.uuid4()
        self.execution_id = uuid.uuid4()
        self.workflow_id = uuid.uuid4()
        self.principal = CurrentPrincipal(
            subject="studio-agent",
            tenant_id=str(self.tenant_id),
            roles=["core_rpa_agent"],
            claims={},
        )
        self.bot = SimpleNamespace(
            id=self.bot_id,
            tenant_id=self.tenant_id,
            registered_by=self.principal.subject,
            status="IDLE",
            capabilities=["runtime:AIS"],
            last_heartbeat_at=None,
        )
        self.execution = SimpleNamespace(
            id=self.execution_id,
            tenant_id=self.tenant_id,
            workflow_id=self.workflow_id,
            workflow_version=2,
            status="QUEUED",
            bot_id=None,
            input_data={"text": "safe sample"},
            started_at=None,
            finished_at=None,
            result_data=None,
            error_message=None,
        )
        self.queue_item = SimpleNamespace(
            tenant_id=self.tenant_id,
            execution_id=self.execution_id,
            status="READY",
            available_at=datetime.now(timezone.utc),
            priority=5,
            created_at=datetime.now(timezone.utc),
            attempts=0,
        )
        self.workflow = SimpleNamespace(
            id=self.workflow_id,
            tenant_id=self.tenant_id,
            status="PUBLISHED",
            version=2,
            definition={
                "runtime": "AIS",
                "contract_version": 1,
                "steps": [{"type": "set_variable", "key": "ok", "value": True}],
            },
        )

    def test_agent_claim_rechecks_license_and_uses_fenced_queue_attempt(self) -> None:
        db = Mock()
        db.scalar.side_effect = [self.bot, self.execution, self.workflow]
        db.scalars.return_value = [self.queue_item]
        with (
            patch("app.modules.automation.bots.router.require_active_license") as license_check,
            patch("app.modules.automation.bots.router.record_audit", return_value=object()),
        ):
            claim = claim_studio_execution(self.bot_id, db, self.principal)

        license_check.assert_called_once_with(db, self.tenant_id)
        self.assertEqual(claim.runtime, "AIS")
        self.assertEqual(claim.claim_attempt, 1)
        self.assertEqual(self.queue_item.status, "CLAIMED")
        self.assertEqual(self.execution.status, "RUNNING")
        self.assertEqual(self.bot.status, "BUSY")
        db.commit.assert_called_once()

    def test_stale_agent_claim_cannot_complete_after_requeue(self) -> None:
        db = Mock()
        self.execution.status = "RUNNING"
        self.execution.bot_id = self.bot_id
        self.queue_item.status = "CLAIMED"
        self.queue_item.attempts = 2
        db.scalar.side_effect = [self.execution, self.queue_item]
        payload = RuntimeCompletionCreate(
            claim_attempt=1,
            status="SUCCEEDED",
            result_data={"variables": {}},
        )
        with patch(
            "app.modules.automation.bots.router.get_tenant_resource",
            return_value=self.bot,
        ), self.assertRaises(HTTPException) as raised:
            complete_studio_execution(self.bot_id, self.execution_id, payload, db, self.principal)

        self.assertEqual(raised.exception.status_code, 409)
        db.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
