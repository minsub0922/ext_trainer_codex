"""Compatibility notes for adapting canonical exports to OLMo-family runs."""

from __future__ import annotations


def describe_conversion_path() -> dict:
    return {
        "reusable": [
            "canonical schema",
            "unified merger/splitter",
            "llamafactory export",
            "dataset registry generation",
        ],
        "model_specific": [
            "chat template validation",
            "tokenizer special token checks",
            "recommended LoRA target modules",
        ],
        "limitations": [
            "Current PoC uses a placeholder OLMo-family checkpoint entry.",
            "Prompt template and tokenizer behavior must be validated before production runs.",
        ],
    }
