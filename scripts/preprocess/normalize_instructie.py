#!/usr/bin/env python3
"""Normalize InstructIE raw files into canonical JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.common.io import read_json, read_jsonl, write_jsonl
from src.common.schema import compute_dataset_stats
from src.datasets.instructie.converter import convert_instructie_rows
from src.datasets.instructie.downloader import InstructIEDownloader
from src.datasets.instructie.parser import parse_instructie_record


def _candidate_split_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.jsonl") if path.is_file())


def _resolve_stale_html_input(path: Path, split: str | None) -> tuple[Path | None, list[Path]]:
    candidates = _candidate_split_files(path.parent)
    if not candidates:
        return None, []
    if split:
        split_match = path.parent / f"{split}.jsonl"
        if split_match.exists():
            return split_match, candidates
    train_match = path.parent / "train.jsonl"
    if train_match.exists():
        return train_match, candidates
    if len(candidates) == 1:
        return candidates[0], candidates
    return None, candidates


def _bootstrap_instructie_split(directory: Path, split: str | None) -> Path | None:
    desired_split = split or "train"
    downloader = InstructIEDownloader(
        root_dir=directory,
        dataset_id="zjunlp/InstructIE",
        split=desired_split,
    )
    result = downloader.run(dry_run=False)
    print(result.message)
    target = directory / f"{desired_split}.jsonl"
    return target if target.exists() else None


def load_rows(path: Path, split: str | None) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}. "
            "Check the filename and prefer the real downloaded asset path, for example "
            "'data/raw/instructie/train.jsonl'."
        )
    if path.suffix == ".jsonl":
        rows = read_jsonl(path)
    else:
        try:
            payload = read_json(path)
        except json.JSONDecodeError as exc:
            preview = path.read_text(encoding="utf-8", errors="ignore")[:200].strip().replace("\n", " ")
            resolved_path, candidates = _resolve_stale_html_input(path, split)
            if resolved_path is not None:
                print(
                    f"Input {path} is a stale HTML page. "
                    f"Falling back to detected dataset split file: {resolved_path}"
                )
                return load_rows(resolved_path, split)
            if path.name == "instructie_raw.json":
                print(
                    f"Input {path} is a stale HTML page and no local split files were found. "
                    "Attempting to download the requested InstructIE split via Hugging Face datasets."
                )
                bootstrapped_path = _bootstrap_instructie_split(path.parent, split)
                if bootstrapped_path is not None:
                    print(f"Recovered by downloading split file: {bootstrapped_path}")
                    return load_rows(bootstrapped_path, split)
            candidate_text = ", ".join(str(candidate) for candidate in candidates) if candidates else "none found"
            raise ValueError(
                f"Input file is not valid JSON: {path}. "
                f"Preview: {preview!r}. "
                "This usually means the downloader saved an HTML page instead of a raw dataset asset. "
                f"Detected sibling JSONL files: {candidate_text}. "
                "Prefer a real split file such as 'data/raw/instructie/train.jsonl'."
            ) from exc
        rows = payload if isinstance(payload, list) else payload.get("data", [])
    if not isinstance(rows, list):
        raise ValueError(f"Expected a list-like dataset payload in {path}, got {type(rows).__name__}.")
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
