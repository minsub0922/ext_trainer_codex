"""Downloader for InstructIE dataset assets."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

import requests

from src.common.io import read_json, read_jsonl, write_jsonl
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

    def __init__(
        self,
        root_dir: Path,
        source_url: str | None = None,
        dataset_id: str | None = None,
        config_name: str | None = None,
        split: str | None = None,
    ):
        super().__init__(root_dir)
        self.source_url = source_url
        self.dataset_id = dataset_id
        self.config_name = config_name
        self.split = split

    @staticmethod
    def _infer_hf_dataset_id(source_url: str | None) -> str | None:
        if not source_url:
            return None
        marker = "huggingface.co/datasets/"
        if marker not in source_url:
            return None
        suffix = source_url.split(marker, 1)[1].strip("/")
        return suffix.split("/tree/", 1)[0].split("/resolve/", 1)[0]

    @staticmethod
    def _normalize_split_name(name: str) -> str:
        lowered = name.lower()
        if "train" in lowered:
            return "train"
        if "valid" in lowered or "dev" in lowered:
            return "dev"
        if "test" in lowered:
            return "test"
        return "other"

    @staticmethod
    def _read_raw_rows(path: Path) -> list[dict[str, Any]]:
        if path.suffix.lower() == ".jsonl":
            return read_jsonl(path)
        if path.suffix.lower() == ".json":
            try:
                payload = read_json(path)
            except json.JSONDecodeError as exc:
                # Some upstream files use a .json suffix but are actually JSONL / NDJSON.
                if "Extra data" in str(exc):
                    return read_jsonl(path)
                raise
            if isinstance(payload, list):
                return payload
            if isinstance(payload, dict):
                for key in ("data", "examples", "items"):
                    if isinstance(payload.get(key), list):
                        return payload[key]
            raise ValueError(f"Unsupported JSON structure in {path}")
        raise ValueError(f"Unsupported raw file format: {path}")

    def _download_via_hf_datasets(self, dataset_id: str) -> DownloadResult:
        try:
            from huggingface_hub import hf_hub_download, list_repo_files
        except ImportError as exc:
            raise ImportError(
                "The 'huggingface_hub' package is required for Hugging Face dataset downloads. "
                "Install dependencies with 'pip install -r requirements.txt'."
            ) from exc

        repo_files = list_repo_files(repo_id=dataset_id, repo_type="dataset")
        candidate_files = [
            file_name
            for file_name in repo_files
            if file_name.lower().endswith((".json", ".jsonl")) and not Path(file_name).name.startswith(".")
        ]
        if not candidate_files:
            raise FileNotFoundError(f"No JSON/JSONL files found in Hugging Face dataset repo '{dataset_id}'.")

        split_buckets: dict[str, list[dict[str, Any]]] = {"train": [], "dev": [], "test": []}
        downloaded_files: list[str] = []
        desired_split = self._normalize_split_name(self.split or "train") if self.split else None
        for file_name in candidate_files:
            normalized_split = self._normalize_split_name(file_name)
            if desired_split and normalized_split != desired_split:
                continue
            if normalized_split == "other":
                continue
            local_path = Path(
                hf_hub_download(
                    repo_id=dataset_id,
                    repo_type="dataset",
                    filename=file_name,
                )
            )
            rows = self._read_raw_rows(local_path)
            split_buckets[normalized_split].extend(rows)
            downloaded_files.append(file_name)

        saved_files: list[str] = []
        for split_name, rows in split_buckets.items():
            if not rows:
                continue
            target = self.root_dir / f"{split_name}.jsonl"
            write_jsonl(target, rows)
            saved_files.append(str(target))

        if desired_split and not split_buckets[desired_split]:
            raise FileNotFoundError(
                f"No raw files matching split '{desired_split}' were found in dataset '{dataset_id}'. "
                f"Candidate files inspected: {', '.join(candidate_files)}"
            )
        if not saved_files:
            raise FileNotFoundError(
                f"Could not materialize any split files from dataset '{dataset_id}'. "
                f"Candidate files inspected: {', '.join(candidate_files)}"
            )

        stale_raw_file = self.root_dir / "instructie_raw.json"
        if stale_raw_file.exists():
            stale_raw_file.unlink()

        return DownloadResult(
            dataset_name=self.dataset_name,
            target_dir=self.root_dir,
            downloaded=True,
            message=(
                f"Downloaded raw Hugging Face dataset files from '{dataset_id}' into {self.root_dir}. "
                f"Aggregated files: {', '.join(saved_files)}. "
                f"Source files: {', '.join(downloaded_files)}"
            ),
        )

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
            2. Prefer Hugging Face dataset download by dataset id when available.
            3. Download JSON/JSONL assets into this directory manually if network access is restricted.
            4. Run scripts/preprocess/normalize_instructie.py to convert to canonical JSONL.
            """
        ).strip()
        note_path.write_text(note_body + "\n", encoding="utf-8")

        inferred_dataset_id = self.dataset_id or self._infer_hf_dataset_id(self.source_url)

        if dry_run or (not self.source_url and not inferred_dataset_id):
            return DownloadResult(
                dataset_name=self.dataset_name,
                target_dir=self.root_dir,
                downloaded=False,
                message="Wrote dataset note only. Provide --dataset-id, a Hugging Face dataset URL, or a direct asset URL.",
            )

        if inferred_dataset_id:
            return self._download_via_hf_datasets(inferred_dataset_id)

        target_file = self.root_dir / "instructie_raw.json"
        response = requests.get(self.source_url, timeout=60)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        preview = response.text[:512].lstrip() if response.text else ""
        if "text/html" in content_type or preview.startswith("<!DOCTYPE html") or preview.startswith("<html"):
            raise ValueError(
                "The provided --source-url returned an HTML page, not a raw JSON/JSONL asset. "
                "If you used a Hugging Face dataset page URL, use --dataset-id zjunlp/InstructIE "
                "or pass that dataset page URL directly so the downloader can use the datasets library."
            )
        target_file.write_bytes(response.content)
        return DownloadResult(
            dataset_name=self.dataset_name,
            target_dir=self.root_dir,
            downloaded=True,
            message=f"Downloaded InstructIE asset to {target_file}",
        )
