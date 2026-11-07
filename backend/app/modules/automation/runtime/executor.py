from collections.abc import Mapping
from typing import Any

from app.modules.automation.runtime.engine import execute_workflow


def execute_definition(
    definition: Mapping[str, Any],
    input_data: Mapping[str, Any],
) -> dict[str, Any]:
    return execute_workflow(definition, input_data)
