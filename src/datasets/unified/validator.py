"""Validation helpers for canonical datasets."""

from __future__ import annotations

from typing import Any

from src.common.schema import validate_canonical_record


def validate_rows(rows: list[dict[str, Any]], strict: bool = True) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for row in rows:
        item = validate_canonical_record(row, strict=False)
        if item is None:
            invalid.append(row)
        else:
            valid.append(item.model_dump_safe())
    if strict and invalid:
        raise ValueError(f"Found {len(invalid)} invalid rows.")
    return valid, invalid
