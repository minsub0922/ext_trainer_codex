from src.scripts_export_helpers import export_llamafactory_rows_for_test


def test_export_to_llamafactory_unified() -> None:
    exported = export_llamafactory_rows_for_test(
        [
            {
                "id": "1",
                "text": "Alice joined Contoso.",
                "lang": "en",
                "source": "demo",
                "task_types": ["entity", "relation"],
                "schema": {"kv": [], "entity": ["PERSON", "ORG"], "relation": ["works_for"]},
                "answer": {
                    "kv": {},
                    "entity": [{"text": "Alice", "type": "PERSON", "start": 0, "end": 5}],
                    "relation": [{"head": "Alice", "head_type": "PERSON", "relation": "works_for", "tail": "Contoso", "tail_type": "ORG"}],
                },
                "meta": {"dataset": "demo", "license": "UNKNOWN", "split": "train", "notes": "", "default_enabled": True},
            }
        ]
    )
    assert exported[0]["instruction"]
    assert exported[0]["output"].startswith("{")
