"""Canonical IE schema and validation logic."""

from __future__ import annotations

from collections import Counter
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from src.common.constants import SUPPORTED_SPLITS, SUPPORTED_TASK_TYPES

TaskType = Literal["kv", "entity", "relation"]
SplitType = Literal["train", "dev", "test"]


class EntityAnnotation(BaseModel):
    text: str
    type: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_span(self) -> "EntityAnnotation":
        if self.end <= self.start:
            raise ValueError("Entity end must be greater than start.")
        return self


class RelationAnnotation(BaseModel):
    head: str
    head_type: str | None = None
    relation: str
    tail: str
    tail_type: str | None = None


class CanonicalSchemaSpec(BaseModel):
    kv: list[str] = Field(default_factory=list)
    entity: list[str] = Field(default_factory=list)
    relation: list[str] = Field(default_factory=list)


class CanonicalAnswer(BaseModel):
    kv: dict[str, Any] = Field(default_factory=dict)
    entity: list[EntityAnnotation] = Field(default_factory=list)
    relation: list[RelationAnnotation] = Field(default_factory=list)


class CanonicalMeta(BaseModel):
    dataset: str
    license: str = "UNKNOWN"
    split: SplitType | None = None
    notes: str = ""
    default_enabled: bool = True

    @field_validator("split")
    @classmethod
    def validate_split(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in SUPPORTED_SPLITS:
            raise ValueError(f"Unsupported split: {value}")
        return value


class CanonicalExample(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    text: str
    lang: str
    source: str
    task_types: list[TaskType]
    schema_: CanonicalSchemaSpec = Field(alias="schema", serialization_alias="schema")
    answer: CanonicalAnswer = Field(default_factory=CanonicalAnswer)
    meta: CanonicalMeta

    @field_validator("task_types")
    @classmethod
    def validate_task_types(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("task_types must not be empty.")
        invalid = [item for item in value if item not in SUPPORTED_TASK_TYPES]
        if invalid:
            raise ValueError(f"Unsupported task_types: {invalid}")
        return sorted(set(value), key=value.index)

    @model_validator(mode="after")
    def validate_contract(self) -> "CanonicalExample":
        task_set = set(self.task_types)
        if "kv" in task_set:
            missing_keys = [key for key in self.schema_.kv if key not in self.answer.kv]
            if missing_keys:
                for key in missing_keys:
                    self.answer.kv[key] = None
        if "entity" not in task_set and self.answer.entity:
            raise ValueError("Entity answer present without entity task.")
        if "relation" not in task_set and self.answer.relation:
            raise ValueError("Relation answer present without relation task.")
        return self

    def model_dump_safe(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def validate_canonical_record(payload: dict[str, Any], strict: bool = True) -> CanonicalExample | None:
    try:
        return CanonicalExample.model_validate(payload)
    except ValidationError:
        if strict:
            raise
        return None


def compute_dataset_stats(rows: list[dict[str, Any] | CanonicalExample]) -> dict[str, Any]:
    validated: list[CanonicalExample] = []
    for row in rows:
        validated.append(row if isinstance(row, CanonicalExample) else CanonicalExample.model_validate(row))

    task_counter: Counter[str] = Counter()
    split_counter: Counter[str] = Counter()
    lang_counter: Counter[str] = Counter()
    dataset_counter: Counter[str] = Counter()

    for item in validated:
        task_counter.update(item.task_types)
        lang_counter.update([item.lang])
        dataset_counter.update([item.meta.dataset])
        if item.meta.split:
            split_counter.update([item.meta.split])

    return {
        "num_examples": len(validated),
        "task_counts": dict(task_counter),
        "split_counts": dict(split_counter),
        "language_counts": dict(lang_counter),
        "dataset_counts": dict(dataset_counter),
    }
