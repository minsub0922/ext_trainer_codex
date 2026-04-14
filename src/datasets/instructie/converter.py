"""Convert parsed InstructIE rows into canonical examples."""

from __future__ import annotations

from typing import Any
from pydantic import ValidationError

from src.common.io import sha1_text
from src.common.schema import (
    CanonicalAnswer,
    CanonicalExample,
    CanonicalMeta,
    CanonicalSchemaSpec,
    EntityAnnotation,
    RelationAnnotation,
)


def _safe_entity_annotations(items: list[dict[str, Any]]) -> list[EntityAnnotation]:
    entities: list[EntityAnnotation] = []
    for item in items:
        if not item:
            continue
        try:
            entities.append(EntityAnnotation.model_validate(item))
        except ValidationError:
            continue
    return entities


def convert_instructie_record(payload: dict[str, Any]) -> CanonicalExample:
    task_types: list[str] = []
    entities = _safe_entity_annotations(payload.get("entity_annotations", []))
    relations = [RelationAnnotation.model_validate(item) for item in payload.get("relation_annotations", []) if item]
    if entities:
        task_types.append("entity")
    if relations:
        task_types.append("relation")
    if not task_types:
        task_types = ["relation"]

    record_id = payload.get("id") or f"instructie-{sha1_text(payload.get('text', ''))[:12]}"
    notes = "Entity annotations may only exist for a subset of files or splits. Relation extraction is first-class."
    return CanonicalExample(
        id=record_id,
        text=payload["text"],
        lang=payload.get("lang", "en"),
        source="instructie",
        task_types=task_types,
        schema=CanonicalSchemaSpec(
            entity=payload.get("entity_schema", []),
            relation=payload.get("relation_schema", []),
        ),
        answer=CanonicalAnswer(entity=entities, relation=relations),
        meta=CanonicalMeta(
            dataset="instructie",
            license="TODO_VERIFY",
            split=payload.get("split"),
            notes=notes,
            default_enabled=True,
        ),
    )


def convert_instructie_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [convert_instructie_record(row).model_dump_safe() for row in rows]
