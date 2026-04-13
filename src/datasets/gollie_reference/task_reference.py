"""GoLLIE-inspired task descriptions without adding a hard dependency."""

from __future__ import annotations


def build_task_description(task_type: str, labels: list[str]) -> str:
    label_text = ", ".join(labels) if labels else "no predefined labels"
    if task_type == "kv":
        return f"Extract the requested slots as JSON object keys. Allowed fields: {label_text}."
    if task_type == "entity":
        return f"Extract entity mentions using only these labels: {label_text}."
    if task_type == "relation":
        return f"Extract typed relations with this label set: {label_text}."
    raise ValueError(f"Unsupported task_type: {task_type}")
