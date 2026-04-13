"""Test helper shim for export behavior."""

from __future__ import annotations

from typing import Any

from src.training.exporter import export_rows


def export_llamafactory_rows_for_test(rows: list[dict[str, Any]], mode: str = "unified") -> list[dict[str, Any]]:
    return export_rows(rows, mode)
