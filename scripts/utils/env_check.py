#!/usr/bin/env python3
"""Basic environment checks for the PoC repository."""

from __future__ import annotations

import importlib
import os


def main() -> None:
    modules = ["yaml", "pydantic", "requests", "pytest"]
    missing = []
    for name in modules:
        try:
            importlib.import_module(name)
        except ImportError:
            missing.append(name)
    print({"pythonpath": os.environ.get("PYTHONPATH", ""), "missing_modules": missing})
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
