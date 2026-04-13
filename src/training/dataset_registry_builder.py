"""Build LLaMA-Factory dataset registry artifacts."""

from __future__ import annotations

from pathlib import Path

from src.common.io import write_json


def build_dataset_info(dataset_name: str, file_name: str, ranking: bool = False) -> dict:
    return {
        dataset_name: {
            "file_name": file_name,
            "formatting": "alpaca",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output",
            },
            "ranking": ranking,
        }
    }


def write_dataset_info(output_dir: str | Path, dataset_name: str, file_name: str) -> Path:
    output_path = Path(output_dir) / "dataset_info.json"
    write_json(output_path, build_dataset_info(dataset_name, file_name))
    return output_path
