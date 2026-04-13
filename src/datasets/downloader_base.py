"""Base helpers for dataset downloaders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.common.paths import ensure_dir


@dataclass(slots=True)
class DownloadResult:
    dataset_name: str
    target_dir: Path
    downloaded: bool
    message: str


class DatasetDownloader:
    dataset_name = "unknown"

    def __init__(self, root_dir: Path):
        self.root_dir = ensure_dir(root_dir)

    def run(self, dry_run: bool = False) -> DownloadResult:
        raise NotImplementedError
