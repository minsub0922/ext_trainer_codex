"""Downloader for InstructIE dataset assets."""

from __future__ import annotations

import json
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
        return suffix.split("/", 1)[0] if "/" not in suffix else suffix

    def _download_via_hf_datasets(self, dataset_id: str) -> DownloadResult:
        try:
            from datasets import Dataset, DatasetDict, load_dataset
        except ImportError as exc:
            raise ImportError(
                "The 'datasets' package is required for Hugging Face dataset downloads. "
                "Install dependencies with 'pip install -r requirements.txt'."
            ) from exc

        dataset_obj = load_dataset(dataset_id, self.config_name)
        saved_files: list[str] = []
        if isinstance(dataset_obj, DatasetDict):
            split_names = [self.split] if self.split else list(dataset_obj.keys())
            for split_name in split_names:
                if split_name not in dataset_obj:
                    raise KeyError(f"Split '{split_name}' not found in dataset '{dataset_id}'.")
                target = self.root_dir / f"{split_name}.jsonl"
                self._write_hf_split_jsonl(dataset_obj[split_name], target)
                saved_files.append(str(target))
        elif isinstance(dataset_obj, Dataset):
            split_name = self.split or "train"
            target = self.root_dir / f"{split_name}.jsonl"
            self._write_hf_split_jsonl(dataset_obj, target)
            saved_files.append(str(target))
        else:
            raise TypeError(f"Unsupported dataset object: {type(dataset_obj).__name__}")

        return DownloadResult(
            dataset_name=self.dataset_name,
            target_dir=self.root_dir,
            downloaded=True,
            message=(
                f"Downloaded Hugging Face dataset '{dataset_id}' into {self.root_dir}. "
                f"Saved split files: {', '.join(saved_files)}"
            ),
        )

    @staticmethod
    def _write_hf_split_jsonl(dataset_split: object, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            for row in dataset_split:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

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
