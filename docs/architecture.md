# Architecture

The repository is organized around one stable contract: the canonical IE schema in `src/common/schema.py`.

## Core flow

1. Raw datasets are downloaded or staged under `data/raw/`.
2. Dataset-specific parsers normalize source quirks into small intermediate dictionaries.
3. Converters emit canonical JSONL rows.
4. Unified merger and splitter compose multiple canonical datasets into one training-ready dataset.
5. Export scripts transform canonical rows into LLaMA-Factory instruction format.
6. Training scripts run LoRA SFT, evaluation, inference, and optional adapter merge.

## Design choices

- K/V extraction is first-class, not bolted on later.
- GoLLIE is used only as a schema-conditioned IE design reference.
- LLaMA-Factory is treated as a backend, not the source-of-truth data model.
- Model-specific logic is isolated to model registry and config selection.

## Module contracts

- `src/common/`: paths, IO, logging, schema, constants.
- `src/datasets/`: download, parse, convert, merge, validate.
- `src/training/`: export, registry creation, config merging, command wrappers.
- `src/models/`: model-family defaults.
- `src/olmo3_poc/`: future OLMo-family integration notes and adapter.
