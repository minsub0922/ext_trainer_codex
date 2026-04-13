"""Downloader for InstructIE dataset assets."""

from __future__ import annotations

import textwrap
from pathlib import Path

import requests

from src.datasets.downloader_base import DatasetDownloader, DownloadResult
from src.datasets.metadata import DatasetNote


INSTRUCTIE_NOTE = DatasetNote(
    name="instructie",
    source="Public seed IE dataset. User must confirm the exact upstream release for internal use.",
    expected_task_types=["entity", "relation"],
    license="TODO_VERIFY",
    default_enabled=True,
    usage_mode="public_seed",
)


class InstructIEDownloader(DatasetDownloader):
    dataset_name = "instructie"

    def __init__(self, root_dir: Path, source_url: str | None = None):
        super().__init__(root_dir)
        self.source_url = source_url

    def run(self, dry_run: bool = False) -> DownloadResult:
        note_path = self.root_dir / "README.instructie.txt"
        note_body = textwrap.dedent(
            f"""
            dataset: {INSTRUCTIE_NOTE.name}
            source: {INSTRUCTIE_NOTE.source}
            expected_task_types: {",".join(INSTRUCTIE_NOTE.expected_task_types)}
            license: {INSTRUCTIE_NOTE.license}
            default_enabled: {INSTRUCTIE_NOTE.default_enabled}

            Preferred flow:
            1. Review the upstream dataset license and source files.
            2. Download JSON/JSONL assets into this directory manually if network access is restricted.
            3. Run scripts/preprocess/normalize_instructie.py to convert to canonical JSONL.
            """
        ).strip()
        note_path.write_text(note_body + "\n", encoding="utf-8")

        if dry_run or not self.source_url:
            return DownloadResult(
                dataset_name=self.dataset_name,
                target_dir=self.root_dir,
                downloaded=False,
                message="Wrote dataset note only. Provide --source-url to attempt direct download.",
            )

        target_file = self.root_dir / "instructie_raw.json"
        response = requests.get(self.source_url, timeout=60)
        response.raise_for_status()
        target_file.write_bytes(response.content)
        return DownloadResult(
            dataset_name=self.dataset_name,
            target_dir=self.root_dir,
            downloaded=True,
            message=f"Downloaded InstructIE asset to {target_file}",
        )
