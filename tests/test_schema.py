from src.common.schema import CanonicalExample


def test_canonical_schema_accepts_mixed_tasks() -> None:
    item = CanonicalExample.model_validate(
        {
            "id": "x",
            "text": "Alice works at Acme.",
            "lang": "en",
            "source": "test",
            "task_types": ["kv", "entity", "relation"],
            "schema": {"kv": ["employer"], "entity": ["PERSON", "ORG"], "relation": ["works_for"]},
            "answer": {
                "kv": {"employer": "Acme"},
                "entity": [{"text": "Alice", "type": "PERSON", "start": 0, "end": 5}],
                "relation": [{"head": "Alice", "head_type": "PERSON", "relation": "works_for", "tail": "Acme", "tail_type": "ORG"}],
            },
            "meta": {"dataset": "demo", "license": "UNKNOWN", "split": "train", "notes": "", "default_enabled": True},
        }
    )
    assert item.answer.kv["employer"] == "Acme"
