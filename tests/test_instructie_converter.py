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
