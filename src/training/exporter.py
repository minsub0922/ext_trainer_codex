"""Canonical to LLaMA-Factory export helpers."""

from __future__ import annotations

import json
from typing import Any

from src.common.schema import CanonicalExample
from src.datasets.gollie_reference.schema_patterns import schema_prompt


def build_instruction(example: CanonicalExample, mode: str) -> tuple[str, str, str]:
    task_modes = {
        "kv": "Extract the requested key/value fields from the text.",
        "entity": "Extract typed entities from the text.",
        "relation": "Extract typed relations from the text.",
        "unified": "Extract all requested IE structures from the text using the provided schema.",
    }
    if mode not in task_modes:
        raise ValueError(f"Unsupported export mode: {mode}")

    instruction = (
        f"{task_modes[mode]} Return strict JSON only.\n"
        + schema_prompt(example.schema.model_dump(mode="json"))
    )
    user_input = json.dumps(
        {
            "text": example.text,
            "lang": example.lang,
            "task_types": example.task_types,
            "schema": example.schema.model_dump(mode="json"),
        },
        ensure_ascii=False,
    )
    output = json.dumps(example.answer.model_dump(mode="json"), ensure_ascii=False)
    return instruction, user_input, output


def export_rows(rows: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    exported: list[dict[str, Any]] = []
    for row in rows:
        example = CanonicalExample.model_validate(row)
        if mode != "unified" and mode not in example.task_types:
            continue
        instruction, user_input, output = build_instruction(example, mode)
        exported.append(
            {
                "id": example.id,
                "instruction": instruction,
                "input": user_input,
                "output": output,
                "system": instruction,
                "history": [],
            }
        )
    return exported
