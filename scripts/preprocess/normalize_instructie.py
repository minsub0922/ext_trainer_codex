#!/usr/bin/env python3
"""Normalize InstructIE raw files into canonical JSONL."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.io import read_json, read_jsonl, write_jsonl
from src.common.schema import compute_dataset_stats
from src.datasets.instructie.converter import convert_instructie_rows
from src.datasets.instructie.parser import parse_instructie_record


def load_rows(path: Path, split: str | None) -> list[dict]:
    if path.suffix == ".jsonl":
        rows = read_jsonl(path)
    else:
        payload = read_json(path)
        rows = payload if isinstance(payload, list) else payload.get("data", [])
    return [parse_instructie_record(row, default_split=split) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Raw InstructIE JSON/JSONL file.")
    parser.add_argument("--output", required=True, help="Canonical JSONL output path.")
    parser.add_argument("--split", default=None, help="Optional default split label.")
    parser.add_argument("--stats-only", action="store_true", help="Print stats without writing output.")
    args = parser.parse_args()

    parsed_rows = load_rows(Path(args.input), args.split)
    canonical_rows = convert_instructie_rows(parsed_rows)
    print(compute_dataset_stats(canonical_rows))
    if not args.stats_only:
        write_jsonl(args.output, canonical_rows)
        print(f"Wrote {len(canonical_rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
