from concurrent.futures import ThreadPoolExecutor
from collections.abc import Mapping, Sequence
from typing import Any


SUPPORTED_ACTIONS = (
    "set_variable",
    "condition",
    "for_each",
    "while",
    "parallel",
    "component",
    "log",
)
UNSUPPORTED_INTEGRATION_ACTIONS = (
    "api_request",
    "browser",
    "database",
    "document",
    "file",
    "desktop",
)
MAX_STEPS = 200
MAX_LOOP_ITEMS = 100
MAX_NESTING = 8
MAX_PARALLEL_BRANCHES = 4
MAX_STUDIO_RULES = 200
STUDIO_RUNTIMES = {"AIS", "CY"}


def validate_studio_definition(definition: Mapping[str, Any]) -> str:
    runtime = definition.get("runtime")
    if not isinstance(runtime, str) or runtime not in STUDIO_RUNTIMES:
        raise WorkflowValidationError("Workflow runtime must be AIS or CY.")
    if type(definition.get("contract_version")) is not int or definition["contract_version"] != 1:
        raise WorkflowValidationError("Studio workflow contract_version must be 1.")

    if runtime == "AIS":
        steps = definition.get("steps")
        if not isinstance(steps, list) or len(steps) > MAX_STEPS:
            raise WorkflowValidationError(
                f"AIS workflows require a steps array with at most {MAX_STEPS} entries."
            )
        for index, step in enumerate(steps):
            if not isinstance(step, Mapping):
                raise WorkflowValidationError(f"AIS step {index + 1} must be an object.")
            action = step.get("type")
            if action == "set_variable":
                if set(step) != {"type", "key", "value"}:
                    raise WorkflowValidationError(
                        f"AIS set_variable step {index + 1} contains unsupported fields."
                    )
                key = step.get("key")
                if not isinstance(key, str) or not key or len(key) > 64 or "value" not in step:
                    raise WorkflowValidationError(
                        f"AIS set_variable step {index + 1} requires a key and value."
                    )
            elif action == "prompt":
                if set(step) != {"type", "key", "prompt"}:
                    raise WorkflowValidationError(
                        f"AIS prompt step {index + 1} contains unsupported fields."
                    )
                key = step.get("key")
                prompt = step.get("prompt")
                if (
                    not isinstance(key, str)
                    or not key
                    or len(key) > 64
                    or not isinstance(prompt, str)
                    or not prompt
                    or len(prompt) > 8000
                ):
                    raise WorkflowValidationError(
                        f"AIS prompt step {index + 1} requires a key and prompt of at most 8000 characters."
                    )
            else:
                raise WorkflowValidationError(
                    f"AIS step {index + 1} uses unsupported action '{action}'."
                )
        return runtime

    rules = definition.get("rules")
    if not isinstance(rules, list) or len(rules) > MAX_STUDIO_RULES:
        raise WorkflowValidationError(
            f"CY workflows require a rules array with at most {MAX_STUDIO_RULES} entries."
        )
    for index, rule in enumerate(rules):
        if not isinstance(rule, Mapping):
            raise WorkflowValidationError(f"CY rule {index + 1} must be an object.")
        if set(rule) != {
            "id",
            "field",
            "equals",
            "severity",
            "title",
            "recommended_response",
        }:
            raise WorkflowValidationError(f"CY rule {index + 1} contains unsupported fields.")
        for field, max_length in (
            ("id", 120),
            ("field", 120),
            ("title", 160),
            ("recommended_response", 500),
        ):
            value = rule.get(field)
            if not isinstance(value, str) or not value or len(value) > max_length:
                raise WorkflowValidationError(
                    f"CY rule {index + 1} requires a {field} of at most {max_length} characters."
                )
        path_parts = rule["field"].split(".")
        if any(
            not part
            or not all(character.isascii() and (character.isalnum() or character in "_-") for character in part)
            for part in path_parts
        ):
            raise WorkflowValidationError(
                f"CY rule {index + 1} field must be a dotted property path."
            )
        severity = rule.get("severity")
        if not isinstance(severity, str) or severity not in {
            "INFO",
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }:
            raise WorkflowValidationError(f"CY rule {index + 1} has an unsupported severity.")
        if "equals" not in rule:
            raise WorkflowValidationError(f"CY rule {index + 1} requires an equals value.")
    return runtime


class WorkflowValidationError(ValueError):
    pass


class WorkflowExecutionError(RuntimeError):
    pass


def validate_steps(
    steps: Any,
    *,
    depth: int = 0,
    parallel_depth: int = 0,
) -> list[dict[str, Any]]:
    if depth > MAX_NESTING:
        raise WorkflowValidationError(f"Workflow nesting exceeds {MAX_NESTING} levels.")
    if not isinstance(steps, list):
        raise WorkflowValidationError("Workflow definition must contain a steps array.")
    if len(steps) > MAX_STEPS:
        raise WorkflowValidationError(f"A workflow may contain at most {MAX_STEPS} steps per level.")

    validated: list[dict[str, Any]] = []
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise WorkflowValidationError(f"Step {index + 1} must be an object.")
        action = step.get("type")
        if action in UNSUPPORTED_INTEGRATION_ACTIONS:
            raise WorkflowValidationError(
                f"The '{action}' adapter is not enabled. Register and approve a supported "
                "connector before using external-system actions."
            )
        if action not in SUPPORTED_ACTIONS:
            raise WorkflowValidationError(
                f"Step {index + 1} uses unsupported action '{action}'. "
                f"Allowed actions: {', '.join(SUPPORTED_ACTIONS)}."
            )
        if action == "set_variable":
            key = step.get("key")
            if not isinstance(key, str) or not key or len(key) > 64:
                raise WorkflowValidationError(f"Step {index + 1} requires a variable key (1-64 characters).")
            if "value" not in step:
                raise WorkflowValidationError(f"Step {index + 1} requires a value.")
        elif action == "condition":
            if not isinstance(step.get("variable"), str) or not step["variable"]:
                raise WorkflowValidationError(f"Step {index + 1} requires a condition variable.")
            if "equals" not in step:
                raise WorkflowValidationError(f"Step {index + 1} requires an equals value.")
            validate_steps(step.get("then", []), depth=depth + 1, parallel_depth=parallel_depth)
            validate_steps(step.get("else", []), depth=depth + 1, parallel_depth=parallel_depth)
        elif action in {"for_each", "while"}:
            if not isinstance(step.get("variable"), str) or not step["variable"]:
                raise WorkflowValidationError(f"Step {index + 1} requires a loop variable.")
            if action == "while" and "equals" not in step:
                raise WorkflowValidationError(f"Step {index + 1} requires a while condition value.")
            validate_steps(
                step.get("steps", []),
                depth=depth + 1,
                parallel_depth=parallel_depth,
            )
        elif action == "parallel":
            branches = step.get("branches")
            if parallel_depth >= 1:
                raise WorkflowValidationError("Parallel steps cannot be nested.")
            if not isinstance(branches, list) or not 2 <= len(branches) <= MAX_PARALLEL_BRANCHES:
                raise WorkflowValidationError(
                    f"Parallel steps require 2 to {MAX_PARALLEL_BRANCHES} branches."
                )
            for branch in branches:
                validate_steps(
                    branch,
                    depth=depth + 1,
                    parallel_depth=parallel_depth + 1,
                )
        elif action == "component":
            if not isinstance(step.get("name"), str) or not step["name"]:
                raise WorkflowValidationError(f"Step {index + 1} requires a component name.")
        elif action == "log":
            if not isinstance(step.get("message"), str) or len(step["message"]) > 500:
                raise WorkflowValidationError(f"Step {index + 1} requires a message of at most 500 characters.")
        validated.append(step)
    return validated


def validate_definition(definition: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime = definition.get("runtime", "CORE")
    if runtime == "CORE":
        pass
    elif isinstance(runtime, str) and runtime in STUDIO_RUNTIMES:
        validate_studio_definition(definition)
        return []
    else:
        raise WorkflowValidationError(f"Workflow runtime '{runtime}' is not supported.")

    steps = validate_steps(definition.get("steps", []))
    components = definition.get("components", {})
    if not isinstance(components, Mapping):
        raise WorkflowValidationError("Workflow components must be an object.")
    for name, component_steps in components.items():
        if not isinstance(name, str) or not name or name == "__workflow__" or len(name) > 80:
            raise WorkflowValidationError("Reusable component names must contain 1-80 characters.")
        validate_steps(component_steps)

    def component_references(candidate_steps: Sequence[dict[str, Any]]) -> set[str]:
        references: set[str] = set()
        for step in candidate_steps:
            if step["type"] == "component":
                references.add(step["name"])
            elif step["type"] == "condition":
                references.update(component_references(step.get("then", [])))
                references.update(component_references(step.get("else", [])))
            elif step["type"] in {"for_each", "while"}:
                references.update(component_references(step["steps"]))
            elif step["type"] == "parallel":
                for branch in step["branches"]:
                    references.update(component_references(branch))
        return references

    graph = {
        name: component_references(component_steps)
        for name, component_steps in components.items()
    }
    graph["__workflow__"] = component_references(steps)
    if any(reference not in components for refs in graph.values() for reference in refs):
        raise WorkflowValidationError("Workflow references an unknown reusable component.")

    def visit(name: str, visited: set[str], active: set[str]) -> None:
        if name in active:
            raise WorkflowValidationError("Reusable components cannot contain recursive references.")
        if name in visited:
            return
        active.add(name)
        for reference in graph[name]:
            visit(reference, visited, active)
        active.remove(name)
        visited.add(name)

    visited: set[str] = set()
    for component_name in graph:
        if component_name != "__workflow__":
            visit(component_name, visited, set())
    return steps


def execute_workflow(
    definition: Mapping[str, Any],
    input_data: Mapping[str, Any],
) -> dict[str, Any]:
    steps = validate_definition(definition)
    components = definition.get("components", {})

    def run_steps(
        current_steps: Sequence[dict[str, Any]],
        initial_context: Mapping[str, Any],
        depth: int = 0,
        parallel_depth: int = 0,
    ) -> tuple[dict[str, Any], list[str], int]:
        if depth > MAX_NESTING:
            raise WorkflowExecutionError("Workflow component nesting limit exceeded.")
        context = dict(initial_context)
        logs: list[str] = []
        operation_count = 0
        for step in current_steps:
            operation_count += 1
            action = step["type"]
            if action == "set_variable":
                context[step["key"]] = step["value"]
            elif action == "condition":
                branch = step["then"] if context.get(step["variable"]) == step["equals"] else step["else"]
                context, branch_logs, branch_count = run_steps(
                    branch, context, depth + 1, parallel_depth
                )
                logs.extend(branch_logs)
                operation_count += branch_count
            elif action == "for_each":
                items = context.get(step["variable"])
                if not isinstance(items, list):
                    raise WorkflowExecutionError(
                        f"Variable '{step['variable']}' must be an array for a for_each step."
                    )
                if len(items) > MAX_LOOP_ITEMS:
                    raise WorkflowExecutionError(
                        f"for_each is limited to {MAX_LOOP_ITEMS} items per iteration."
                    )
                original_item = context.get("item")
                had_item = "item" in context
                for item in items:
                    iteration_context = dict(context)
                    iteration_context["item"] = item
                    context, iteration_logs, iteration_count = run_steps(
                        step["steps"], iteration_context, depth + 1, parallel_depth
                    )
                    logs.extend(iteration_logs)
                    operation_count += iteration_count
                if had_item:
                    context["item"] = original_item
                else:
                    context.pop("item", None)
            elif action == "while":
                iteration_count = 0
                while context.get(step["variable"]) == step["equals"]:
                    if iteration_count >= MAX_LOOP_ITEMS:
                        raise WorkflowExecutionError(
                            f"while loops are limited to {MAX_LOOP_ITEMS} iterations."
                        )
                    context, loop_logs, steps_run = run_steps(
                        step["steps"], context, depth + 1, parallel_depth
                    )
                    logs.extend(loop_logs)
                    operation_count += steps_run
                    iteration_count += 1
            elif action == "parallel":
                if parallel_depth >= 1:
                    raise WorkflowExecutionError("Parallel steps cannot be nested.")
                branches = step["branches"]
                with ThreadPoolExecutor(
                    max_workers=len(branches),
                    thread_name_prefix="cyclone-branch",
                ) as executor:
                    branch_results = list(
                        executor.map(
                            lambda branch: run_steps(
                                branch,
                                dict(context),
                                depth + 1,
                                parallel_depth + 1,
                            ),
                            branches,
                        )
                    )
                changed_values: dict[str, Any] = {}
                for branch_context, branch_logs, branch_count in branch_results:
                    for key, value in branch_context.items():
                        if key in context and context[key] == value:
                            continue
                        if key in changed_values and changed_values[key] != value:
                            raise WorkflowExecutionError(
                                f"Parallel branches produced conflicting values for '{key}'."
                            )
                        changed_values[key] = value
                    logs.extend(branch_logs)
                    operation_count += branch_count
                context.update(changed_values)
                if len(logs) > 100:
                    raise WorkflowExecutionError("Workflow log limit exceeded.")
            elif action == "component":
                component_steps = components.get(step["name"])
                if not isinstance(component_steps, list):
                    raise WorkflowExecutionError(f"Reusable component '{step['name']}' was not found.")
                context, component_logs, component_count = run_steps(
                    validate_steps(
                        component_steps,
                        depth=depth + 1,
                        parallel_depth=parallel_depth,
                    ),
                    context,
                    depth + 1,
                    parallel_depth,
                )
                logs.extend(component_logs)
                operation_count += component_count
            elif action == "log":
                if len(logs) >= 100:
                    raise WorkflowExecutionError("Workflow log limit exceeded.")
                logs.append(step["message"])

            if operation_count > MAX_STEPS:
                raise WorkflowExecutionError("Workflow execution step limit exceeded.")
        return context, logs, operation_count

    context, logs, operation_count = run_steps(steps, input_data)
    if operation_count > MAX_STEPS:
        raise WorkflowExecutionError("Workflow execution step limit exceeded.")
    return {"variables": context, "logs": logs, "steps_executed": operation_count}
