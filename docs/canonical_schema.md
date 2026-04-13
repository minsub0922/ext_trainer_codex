# Canonical Schema

The canonical schema is the source of truth for this repository. Every dataset-specific pipeline must convert into this format before merging or training export.

## Why one schema

- K/V extraction, entity extraction, and relation extraction all produce structured outputs.
- One contract simplifies validation, merging, split assignment, stats, and training export.
- The downstream training backend can change later without rewriting dataset pipelines.

## Shape

```json
{
  "id": "sample-1",
  "text": "raw text",
  "lang": "en",
  "source": "dataset_or_system",
  "task_types": ["kv", "entity", "relation"],
  "schema": {
    "kv": ["field_1"],
    "entity": ["ORG"],
    "relation": ["works_for"]
  },
  "answer": {
    "kv": {"field_1": null},
    "entity": [{"text": "Acme", "type": "ORG", "start": 0, "end": 4}],
    "relation": [{"head": "Alice", "head_type": "PERSON", "relation": "works_for", "tail": "Acme", "tail_type": "ORG"}]
  },
  "meta": {
    "dataset": "example",
    "license": "TODO_VERIFY",
    "split": "train",
    "notes": "",
    "default_enabled": true
  }
}
```

## Missing-safe behavior

- K/V fields default to `null` when the task is present but the value is missing.
- Entity and relation arrays default to empty lists.
- Mixed-task examples are valid.
- Entity-only or relation-only examples are valid.

## GoLLIE-inspired framing

- K/V extraction is modeled as slot extraction under `schema.kv`.
- Entity and relation label spaces are explicit ontology constraints.
- Prompting can be schema-conditioned by serializing `schema` directly into the instruction context.
