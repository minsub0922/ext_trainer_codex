"""Parsers for loose InstructIE-like structures."""

from __future__ import annotations

from typing import Any


def _normalize_relation(item: dict[str, Any]) -> dict[str, Any]:
    head = item.get("head") or item.get("subject") or item.get("arg1") or ""
    tail = item.get("tail") or item.get("object") or item.get("arg2") or ""
    relation = item.get("relation") or item.get("predicate") or item.get("label") or ""
    return {
        "head": head,
        "head_type": item.get("head_type") or item.get("subject_type"),
        "relation": relation,
        "tail": tail,
        "tail_type": item.get("tail_type") or item.get("object_type"),
    }


def _normalize_entity(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "text": item.get("text") or item.get("mention") or "",
        "type": item.get("type") or item.get("label") or "",
        "start": int(item.get("start", 0)),
        "end": int(item.get("end", 0)),
    }


def parse_instructie_record(payload: dict[str, Any], default_split: str | None = None) -> dict[str, Any]:
    text = payload.get("text") or payload.get("input") or payload.get("sentence") or ""
    entities = payload.get("entities") or payload.get("entity") or []
    relations = payload.get("relations") or payload.get("relation") or []
    entity_schema = sorted({(item.get("type") or item.get("label") or "") for item in entities if item})
    relation_schema = sorted(
        {(item.get("relation") or item.get("predicate") or item.get("label") or "") for item in relations if item}
    )

    return {
        "id": str(payload.get("id") or payload.get("uid") or payload.get("doc_id") or ""),
        "text": text,
        "lang": payload.get("lang") or payload.get("language") or "en",
        "source": "instructie",
        "split": payload.get("split") or default_split,
        "entity_annotations": [_normalize_entity(item) for item in entities],
        "relation_annotations": [_normalize_relation(item) for item in relations],
        "entity_schema": [item for item in entity_schema if item],
        "relation_schema": [item for item in relation_schema if item],
    }
