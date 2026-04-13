#!/usr/bin/env python3
"""Generate annotation-ready canonical K/V templates from tabular input."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.io import read_yaml, write_jsonl
from src.datasets.internal_kv.template_builder import build_kv_template_rows


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV/JSON/JSONL input.")
    parser.add_argument("--output", required=True, help="Canonical JSONL output.")
    parser.add_argument("--config", default=None, help="Optional YAML config.")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--id-column", default="id")
    parser.add_argument("--language-column", default="lang")
    parser.add_argument("--kv-schema", nargs="+", default=None)
    parser.add_argument("--split", default=None)
    parser.add_argument("--print-example", action="store_true")
    return parser


def main() -> None:
    args = build_argparser().parse_args()
    config = read_yaml(args.config) if args.config else {}
    kv_schema = args.kv_schema or config.get("kv_schema") or ["field_1", "field_2"]
    rows = build_kv_template_rows(
        input_path=args.input,
        text_column=config.get("text_column", args.text_column),
        id_column=config.get("id_column", args.id_column),
        language_column=config.get("language_column", args.language_column),
        kv_schema=kv_schema,
        dataset_name=config.get("dataset_name", "internal_kv_template"),
        source_name=config.get("source_name", "internal"),
        split=args.split or config.get("split"),
    )
    if args.print_example and rows:
        print(rows[0])
    write_jsonl(args.output, rows)
    print(f"Wrote {len(rows)} template rows to {args.output}")


if __name__ == "__main__":
    main()
