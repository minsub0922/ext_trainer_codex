#!/usr/bin/env python3
"""Download or stage InstructIE assets in data/raw."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.paths import data_dir
from src.datasets.instructie.downloader import InstructIEDownloader


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(data_dir("raw", "instructie")), help="Raw dataset directory.")
    parser.add_argument("--source-url", default=None, help="Optional direct asset URL.")
    parser.add_argument("--dry-run", action="store_true", help="Write metadata note only.")
    return parser


def main() -> None:
    args = build_argparser().parse_args()
    downloader = InstructIEDownloader(root_dir=Path(args.output), source_url=args.source_url)
    result = downloader.run(dry_run=args.dry_run)
    print(result.message)


if __name__ == "__main__":
    main()
