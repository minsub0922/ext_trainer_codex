"""Helpers for internal K/V config loading."""

from __future__ import annotations

from pathlib import Path

from src.common.io import read_yaml


def load_internal_kv_config(path: str | Path) -> dict:
    return read_yaml(path)
