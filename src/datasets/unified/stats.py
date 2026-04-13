"""Statistics helpers for unified canonical datasets."""

from __future__ import annotations

from typing import Any

from src.common.schema import compute_dataset_stats


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return compute_dataset_stats(rows)
