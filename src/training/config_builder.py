"""Helpers for loading and rendering training configs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.common.io import read_yaml, write_yaml


def load_config(path: str | Path) -> dict[str, Any]:
    return read_yaml(path)


def merge_configs(*configs: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for config in configs:
        for key, value in config.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
    return merged


def render_training_config(model_cfg: dict[str, Any], sft_cfg: dict[str, Any], overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    rendered = merge_configs(model_cfg, sft_cfg, overrides or {})
    rendered.setdefault("stage", "sft")
    rendered.setdefault("do_train", True)
    rendered.setdefault("finetuning_type", "lora")
    return rendered


def save_training_config(path: str | Path, payload: dict[str, Any]) -> None:
    write_yaml(path, payload)
