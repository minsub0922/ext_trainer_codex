"""Project-wide constants."""

from __future__ import annotations

from pathlib import Path

SUPPORTED_TASK_TYPES = ("kv", "entity", "relation")
SUPPORTED_SPLITS = ("train", "dev", "test")
DEFAULT_RANDOM_SEED = 42
PROJECT_MARKER_FILES = ("README.md", "requirements.txt")
DEFAULT_DATASET_REGISTRY_PATH = Path("data/metadata/dataset_registry.example.yaml")
