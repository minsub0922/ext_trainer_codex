#!/usr/bin/env python3
"""Split canonical JSONL into train/dev/test files."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.io import read_jsonl, write_jsonl
from src.datasets.unified.splitter import assign_splits, split_rows
from src.datasets.unified.stats import summarize_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    if any((row.get("meta") or {}).get("split") for row in rows):
        split_map = split_rows(rows)
    else:
        split_map = split_rows(assign_splits(rows, seed=args.seed))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for split, items in split_map.items():
        target = output_dir / f"{split}.jsonl"
        if target.exists() and not args.overwrite:
            raise FileExistsError(f"{target} exists. Use --overwrite.")
        write_jsonl(target, items)
        print(f"Wrote {len(items)} rows to {target}")
    print(summarize_rows([row for rows in split_map.values() for row in rows]))


if __name__ == "__main__":
    main()
