"""Build annotation-ready canonical K/V skeletons from internal data."""

from __future__ import annotations

from typing import Any

from src.common.io import read_tabular
from src.common.schema import CanonicalAnswer, CanonicalExample, CanonicalMeta, CanonicalSchemaSpec


def build_kv_template_rows(
    input_path: str,
    text_column: str,
    id_column: str,
    language_column: str | None,
    kv_schema: list[str],
    dataset_name: str,
    source_name: str,
    split: str | None = None,
) -> list[dict[str, Any]]:
    rows = read_tabular(input_path)
    result: list[dict[str, Any]] = []
    for raw in rows:
        item_id = str(raw[id_column])
        lang = raw[language_column] if language_column and language_column in raw else "unknown"
        example = CanonicalExample(
            id=item_id,
            text=str(raw[text_column]),
            lang=str(lang),
            source=source_name,
            task_types=["kv"],
            schema=CanonicalSchemaSpec(kv=kv_schema),
            answer=CanonicalAnswer(kv={field: None for field in kv_schema}),
            meta=CanonicalMeta(
                dataset=dataset_name,
                license="INTERNAL",
                split=split,
                notes="Annotation template generated from internal source rows.",
                default_enabled=False,
            ),
        )
        result.append(example.model_dump_safe())
    return result
