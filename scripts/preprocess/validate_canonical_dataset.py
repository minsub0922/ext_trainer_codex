#!/usr/bin/env python3
"""Validate canonical dataset rows."""

from __future__ import annotations

import argparse

from src.common.io import read_jsonl
from src.datasets.unified.validator import validate_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    valid, invalid = validate_rows(read_jsonl(args.input), strict=False)
    print({"valid": len(valid), "invalid": len(invalid)})
    if args.strict and invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
