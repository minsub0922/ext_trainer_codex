"""Evaluation command helpers."""

from __future__ import annotations

import os
import shlex
import subprocess


def run_eval(config_path: str, dry_run: bool = False) -> int:
    cli = os.environ.get("LLAMA_FACTORY_CLI", "llamafactory-cli")
    command = [cli, "eval", config_path]
    print("Command:", shlex.join(command))
    if dry_run:
        return 0
    return subprocess.run(command, check=False).returncode
