import json

import scripts.preprocess.normalize_instructie as normalize_instructie
from scripts.preprocess.normalize_instructie import load_rows
from src.datasets.instructie.downloader import InstructIEDownloader
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


def test_normalizer_bootstraps_hf_download_when_only_stale_html_exists(tmp_path, monkeypatch) -> None:
    stale_file = tmp_path / "instructie_raw.json"
    stale_file.write_text("<!doctype html><html><body>bad</body></html>", encoding="utf-8")
    train_file = tmp_path / "train.jsonl"
    row = {
        "id": "1",
        "text": "Alice joined Contoso.",
        "relations": [{"subject": "Alice", "predicate": "works_for", "object": "Contoso"}],
    }

    def fake_bootstrap(directory, split):
        train_file.write_text(json.dumps(row) + "\n", encoding="utf-8")
        return train_file

    monkeypatch.setattr(normalize_instructie, "_bootstrap_instructie_split", fake_bootstrap)
    loaded = load_rows(stale_file, "train")
    assert loaded[0]["id"] == "1"


def test_instructie_reader_accepts_ndjson_with_json_suffix(tmp_path) -> None:
    raw_file = tmp_path / "train_like.json"
    rows = [
        {"id": "1", "text": "Alice joined Contoso.", "relations": []},
        {"id": "2", "text": "Bob joined Fabrikam.", "relations": []},
    ]
    raw_file.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    loaded = InstructIEDownloader._read_raw_rows(raw_file)
    assert len(loaded) == 2
