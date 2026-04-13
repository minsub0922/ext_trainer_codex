"""Thin wrappers for invoking LLaMA-Factory from shell scripts."""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

from src.training.config_builder import load_config


def resolve_lf_cli() -> str:
    return os.environ.get("LLAMA_FACTORY_CLI", "llamafactory-cli")


def print_config(path: str | Path) -> dict:
    config = load_config(path)
    print(f"Resolved config from {path}:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    return config


def run_train(config_path: str | Path, dry_run: bool = False) -> int:
    command = [resolve_lf_cli(), "train", str(config_path)]
    print("Command:", shlex.join(command))
    if dry_run:
        return 0
    return subprocess.run(command, check=False).returncode
