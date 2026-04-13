"""Dataset registry loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.common.io import read_yaml


def load_dataset_registry(path: str | Path) -> dict[str, Any]:
    return read_yaml(path)
