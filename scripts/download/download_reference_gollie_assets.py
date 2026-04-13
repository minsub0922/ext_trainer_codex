#!/usr/bin/env python3
"""Write reference-only notes for GoLLIE-inspired assets."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="data/raw/gollie_reference", help="Output note directory.")
    args = parser.parse_args()
    path = Path(args.output)
    path.mkdir(parents=True, exist_ok=True)
    body = (
        "dataset: gollie_reference\n"
        "source: GoLLIE paper/repository concepts only\n"
        "expected_task_types: kv,entity,relation\n"
        "license: TODO_VERIFY\n"
        "default_enabled: false\n"
        "mode: reference_only\n"
    )
    (path / "README.gollie_reference.txt").write_text(body, encoding="utf-8")
    print(f"Wrote {path / 'README.gollie_reference.txt'}")


if __name__ == "__main__":
    main()
