"""Reproducible split generation for canonical datasets."""

from __future__ import annotations

import random
from typing import Any

from src.common.schema import CanonicalExample


def assign_splits(
    rows: list[dict[str, Any]],
    seed: int = 42,
    train_ratio: float = 0.8,
    dev_ratio: float = 0.1,
) -> list[dict[str, Any]]:
    if train_ratio <= 0 or dev_ratio < 0 or train_ratio + dev_ratio >= 1:
        raise ValueError("Invalid split ratios.")

    items = [CanonicalExample.model_validate(row).model_dump_safe() for row in rows]
    rng = random.Random(seed)
    rng.shuffle(items)

    total = len(items)
    train_cut = int(total * train_ratio)
    dev_cut = train_cut + int(total * dev_ratio)

    for index, item in enumerate(items):
        if index < train_cut:
            item["meta"]["split"] = "train"
        elif index < dev_cut:
            item["meta"]["split"] = "dev"
        else:
            item["meta"]["split"] = "test"
    return items


def split_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    output = {"train": [], "dev": [], "test": []}
    for row in rows:
        example = CanonicalExample.model_validate(row)
        split = example.meta.split or "train"
        output.setdefault(split, []).append(example.model_dump_safe())
    return output
