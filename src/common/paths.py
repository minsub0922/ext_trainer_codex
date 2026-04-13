"""Path helpers for the repository."""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_dir(*parts: str) -> Path:
    return project_root().joinpath("data", *parts)


def config_dir(*parts: str) -> Path:
    return project_root().joinpath("configs", *parts)


def example_dir(*parts: str) -> Path:
    return project_root().joinpath("examples", *parts)


def docs_dir(*parts: str) -> Path:
    return project_root().joinpath("docs", *parts)
