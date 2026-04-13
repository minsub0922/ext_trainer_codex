"""Schema-conditioned prompt snippets inspired by GoLLIE-style IE."""

from __future__ import annotations

from typing import Any


def schema_prompt(task_schema: dict[str, Any]) -> str:
    return (
        "Use the provided schema as the only valid extraction ontology.\n"
        f"Schema: {task_schema}\n"
        "Return strict JSON and leave missing values as null or empty arrays."
    )
