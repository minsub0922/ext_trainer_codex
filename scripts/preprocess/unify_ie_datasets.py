#!/usr/bin/env python3
"""Merge one or more canonical datasets into a single canonical dataset."""

from __future__ import annotations

import argparse

from src.common.io import read_jsonl, write_json, write_jsonl
from src.datasets.unified.merger import merge_canonical_datasets
from src.datasets.unified.stats import summarize_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True, help="Canonical JSONL files.")
    parser.add_argument("--output", required=True, help="Merged JSONL output.")
    parser.add_argument("--stats-output", default=None, help="Optional stats JSON output.")
    parser.add_argument("--task-types", nargs="*", default=None, help="Filter tasks.")
    args = parser.parse_args()

    datasets = [read_jsonl(path) for path in args.input]
    merged = merge_canonical_datasets(datasets, task_types=args.task_types)
    stats = summarize_rows(merged)
    write_jsonl(args.output, merged)
    if args.stats_output:
        write_json(args.stats_output, stats)
    print(stats)
    print(f"Wrote merged dataset to {args.output}")


if __name__ == "__main__":
    main()
