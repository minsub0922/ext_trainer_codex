#!/usr/bin/env python3
"""Export canonical IE datasets into LLaMA-Factory instruction format."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.io import read_jsonl, write_jsonl
from src.training.dataset_registry_builder import write_dataset_info
from src.training.exporter import export_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True, help="Output directory.")
    parser.add_argument("--mode", choices=["kv", "entity", "relation", "unified"], default="unified")
    parser.add_argument("--dataset-name", default="internal_ie_unified")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    exported = export_rows(rows, args.mode)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{args.dataset_name}.jsonl"
    if out_file.exists() and not args.overwrite:
        raise FileExistsError(f"{out_file} exists. Use --overwrite.")
    write_jsonl(out_file, exported)
    info_file = write_dataset_info(output_dir, args.dataset_name, out_file.name)
    print(f"Wrote {len(exported)} rows to {out_file}")
    print(f"Wrote dataset registry to {info_file}")


if __name__ == "__main__":
    main()
