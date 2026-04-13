"""Merge multiple canonical datasets with stable deduplication."""

from __future__ import annotations

from typing import Any

from src.common.io import sha1_text
from src.common.schema import CanonicalExample


def merge_canonical_datasets(
    datasets: list[list[dict[str, Any]]],
    task_types: list[str] | None = None,
) -> list[dict[str, Any]]:
    seen_ids: set[str] = set()
    seen_text_hashes: set[str] = set()
    merged: list[dict[str, Any]] = []
    allowed = set(task_types or [])

    for rows in datasets:
        for row in rows:
            example = CanonicalExample.model_validate(row)
            if allowed and not (allowed & set(example.task_types)):
                continue
            text_hash = sha1_text(example.text.strip())
            if example.id in seen_ids or text_hash in seen_text_hashes:
                continue
            seen_ids.add(example.id)
            seen_text_hashes.add(text_hash)
            merged.append(example.model_dump_safe())
    return merged
