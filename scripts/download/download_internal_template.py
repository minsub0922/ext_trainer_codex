#!/usr/bin/env python3
"""Create a note for internal dataset onboarding."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="data/raw/internal_placeholder", help="Output directory.")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    note = (
        "dataset: internal_template\n"
        "source: internal company data\n"
        "expected_task_types: kv\n"
        "license: INTERNAL\n"
        "default_enabled: false\n"
        "mode: template_only\n"
    )
    (output / "README.internal_template.txt").write_text(note, encoding="utf-8")
    print(f"Wrote {output / 'README.internal_template.txt'}")


if __name__ == "__main__":
    main()
