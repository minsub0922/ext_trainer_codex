import json

from scripts.preprocess.normalize_instructie import load_rows
from src.datasets.instructie.converter import convert_instructie_record
from src.datasets.instructie.parser import parse_instructie_record


def test_instructie_conversion_handles_relation_first() -> None:
    parsed = parse_instructie_record(
        {
            "id": "1",
            "text": "Alice joined Contoso.",
            "relations": [{"subject": "Alice", "predicate": "works_for", "object": "Contoso"}],
        },
        default_split="train",
    )
    converted = convert_instructie_record(parsed)
    assert converted.meta.split == "train"
    assert "relation" in converted.task_types
    assert converted.answer.relation[0].relation == "works_for"


def test_normalizer_falls_back_from_stale_html_to_train_jsonl(tmp_path) -> None:
    stale_file = tmp_path / "instructie_raw.json"
    stale_file.write_text("<!doctype html><html><body>bad</body></html>", encoding="utf-8")
    train_file = tmp_path / "train.jsonl"
    row = {
        "id": "1",
        "text": "Alice joined Contoso.",
        "relations": [{"subject": "Alice", "predicate": "works_for", "object": "Contoso"}],
    }
    train_file.write_text(json.dumps(row) + "\n", encoding="utf-8")

    loaded = load_rows(stale_file, "train")
    assert loaded[0]["id"] == "1"
