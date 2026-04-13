"""Dataset metadata notes."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class DatasetNote:
    name: str
    source: str
    expected_task_types: list[str]
    license: str
    default_enabled: bool
    usage_mode: str

    def to_dict(self) -> dict:
        return asdict(self)
