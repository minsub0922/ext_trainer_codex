#!/usr/bin/env python3
"""Print canonical dataset statistics."""

from __future__ import annotations

import argparse

from src.common.io import read_jsonl
from src.datasets.unified.stats import summarize_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    print(summarize_rows(read_jsonl(args.input)))


if __name__ == "__main__":
    main()
