from src.datasets.unified.merger import merge_canonical_datasets
from src.datasets.unified.splitter import assign_splits


def test_splitter_is_reproducible() -> None:
    rows = [
        {
            "id": str(idx),
            "text": f"text-{idx}",
            "lang": "en",
            "source": "demo",
            "task_types": ["kv"],
            "schema": {"kv": ["field"], "entity": [], "relation": []},
            "answer": {"kv": {"field": None}, "entity": [], "relation": []},
            "meta": {"dataset": "demo", "license": "UNKNOWN", "split": None, "notes": "", "default_enabled": True},
        }
        for idx in range(20)
    ]
    first = assign_splits(rows, seed=7)
    second = assign_splits(rows, seed=7)
    assert [row["meta"]["split"] for row in first] == [row["meta"]["split"] for row in second]


def test_merger_deduplicates_by_id_or_text() -> None:
    row = {
        "id": "1",
        "text": "duplicate",
        "lang": "en",
        "source": "demo",
        "task_types": ["kv"],
        "schema": {"kv": ["field"], "entity": [], "relation": []},
        "answer": {"kv": {"field": None}, "entity": [], "relation": []},
        "meta": {"dataset": "demo", "license": "UNKNOWN", "split": None, "notes": "", "default_enabled": True},
    }
    merged = merge_canonical_datasets([[row], [{**row, "id": "2"}]])
    assert len(merged) == 1
