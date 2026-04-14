# ext_trainer_codex

A clean, modular PoC repository for internal information extraction SFT research.

This repo is built around one design rule: the canonical IE schema is the source of truth. Raw datasets are normalized into a single task format that supports key-value extraction, entity extraction, and relation extraction, then exported into LLaMA-Factory for supervised fine-tuning, evaluation, inference, and optional LoRA merge workflows.

## What this repository is for

- Running a public-data PoC for internal IE model research
- Onboarding internal K/V datasets with minimal friction
- Keeping data handling explicit and license-sensitive
- Fine-tuning small base models first, with Qwen3 and Qwen3.5 as the default lane
- Leaving a clean extension point for future OLMo3 adoption

## Core ideas

### 1. Canonical schema first

All dataset-specific quirks are converted into one stable JSON structure before training export. That gives you one place for validation, statistics, deduplication, split generation, and downstream reuse.

### 2. K/V extraction is first-class

K/V extraction is not treated as a side case of generic IE. The schema and prompts directly support slot-style extraction so internal document tasks can be handled cleanly.

### 3. LLaMA-Factory is the backend, not the data model

LLaMA-Factory is used for:

- model loading
- dataset registration
- SFT training
- evaluation
- inference
- optional LoRA merge

But the repo does not let the backend dictate the data structure.

### 4. GoLLIE is reference-only

GoLLIE-inspired task structuring is used to inform:

- schema-conditioned prompting
- shared structured output design
- slot/K/V framing
- typed entity and relation definitions

This repo does not depend on GoLLIE as a hard runtime training dependency.

## Supported tasks

- `kv`
- `entity`
- `relation`
- mixed-task examples containing any combination of the above

## Default model path

- `Qwen/Qwen3-0.6B`
- `Qwen/Qwen3.5-0.8B`

The OLMo-family path is intentionally a PoC extension layer, not the default production claim.

## Repository layout

```text
.
├── README.md
├── configs/                  # dataset, model, and SFT YAMLs
├── data/                     # raw, interim, processed, metadata
├── docs/                     # architecture and policy docs
├── examples/                 # synthetic canonical samples and labeling prompts
├── scripts/                  # operator-facing CLIs
├── src/                      # reusable Python modules
├── tests/                    # sanity tests for schema and pipeline behavior
├── Makefile
├── requirements.txt
└── .env.example
```

## Canonical schema

Every dataset is normalized into a structure like this:

```json
{
  "id": "sample-1",
  "text": "Alice joined Contoso in Seoul.",
  "lang": "en",
  "source": "instructie",
  "task_types": ["entity", "relation"],
  "schema": {
    "kv": [],
    "entity": ["PERSON", "ORG", "LOC"],
    "relation": ["works_for", "located_in"]
  },
  "answer": {
    "kv": {},
    "entity": [
      {"text": "Alice", "type": "PERSON", "start": 0, "end": 5}
    ],
    "relation": [
      {"head": "Alice", "head_type": "PERSON", "relation": "works_for", "tail": "Contoso", "tail_type": "ORG"}
    ]
  },
  "meta": {
    "dataset": "instructie",
    "license": "TODO_VERIFY",
    "split": "train",
    "notes": "",
    "default_enabled": true
  }
}
```

See [docs/canonical_schema.md](docs/canonical_schema.md) for the full contract.

## Dataset policy

This repo is intended for internal/company use and treats dataset licensing as an explicit concern.

- InstructIE is included as the default public seed path.
- GoLLIE is reference-only.
- IEPile is not the default final-train path.
- Internal data onboarding is supported, but internal data should stay outside version control.
- Every downloader and onboarding path includes dataset metadata notes:
  - source
  - expected task types
  - license placeholder
  - whether the dataset is default enabled or reference-only

See [docs/dataset_policy.md](docs/dataset_policy.md).

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
make env-check
```

## End-to-end workflow

### 1. Stage or download InstructIE

```bash
python scripts/download/download_instructie.py --dry-run
```

If your environment allows it and you have a verified upstream asset URL:

```bash
python scripts/download/download_instructie.py \
  --source-url "<verified_instructie_asset_url>"
```

Use a direct JSON or JSONL asset URL here, not the Hugging Face dataset landing page URL.

### 2. Normalize InstructIE to canonical JSONL

```bash
python scripts/preprocess/normalize_instructie.py \
  --input data/raw/instructie/instructie_raw.json \
  --output data/processed/instructie_canonical.jsonl \
  --split train
```

### 3. Build an internal K/V annotation template

```bash
python scripts/preprocess/build_internal_kv_template.py \
  --input internal.csv \
  --output data/processed/internal_kv_template.jsonl \
  --config configs/datasets/internal_kv_example.yaml
```

### 4. Merge canonical datasets

```bash
python scripts/preprocess/unify_ie_datasets.py \
  --input data/processed/instructie_canonical.jsonl data/processed/internal_kv_template.jsonl \
  --output data/processed/unified.jsonl \
  --stats-output data/processed/unified_stats.json
```

### 5. Materialize train/dev/test splits

```bash
python scripts/export/export_train_dev_test.py \
  --input data/processed/unified.jsonl \
  --output-dir data/processed/splits \
  --seed 42 \
  --overwrite
```

### 6. Export to LLaMA-Factory format

```bash
python scripts/export/export_to_llamafactory.py \
  --input data/processed/unified.jsonl \
  --output data/processed/llamafactory \
  --mode unified \
  --dataset-name internal_ie_unified \
  --overwrite
```

### 7. Run SFT

```bash
bash scripts/train/run_sft_qwen3.sh
```

### 8. Run eval or inference

```bash
bash scripts/train/run_eval_qwen3.sh
bash scripts/train/run_infer_qwen3.sh
```

### 9. Try the alternate Qwen path

```bash
bash scripts/train/run_sft_qwen35.sh
```

### 10. Inspect the OLMo3 extension path

```bash
bash scripts/train/run_sft_olmo3_poc.sh
```

## Key entry points

### Schema and validation

- `src/common/schema.py`
- `scripts/preprocess/validate_canonical_dataset.py`

### Dataset pipelines

- `scripts/download/download_instructie.py`
- `scripts/preprocess/normalize_instructie.py`
- `scripts/preprocess/build_internal_kv_template.py`
- `scripts/preprocess/unify_ie_datasets.py`

### LLaMA-Factory integration

- `scripts/export/export_to_llamafactory.py`
- `src/training/dataset_registry_builder.py`
- `src/training/config_builder.py`
- `scripts/train/run_sft_qwen3.sh`

### OLMo3 PoC

- `configs/models/olmo3_poc.yaml`
- `configs/sft/olmo3_poc_sft.yaml`
- `src/olmo3_poc/adapter.py`
- `docs/olmo3_extension.md`

## Current assumptions and limitations

- `llamafactory-cli` must already be installed or exposed through `LLAMA_FACTORY_CLI`.
- Dataset license fields are explicit placeholders where the upstream license still needs verification.
- InstructIE entity coverage may depend on the exact upstream asset or split. The docs and converter note this explicitly.
- The OLMo3 path is intentionally honest about its gaps. It is a compatibility sketch, not a production claim.

## Documentation map

- [configs/README.md](configs/README.md)
- [data/README.md](data/README.md)
- [scripts/README.md](scripts/README.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/canonical_schema.md](docs/canonical_schema.md)
- [docs/dataset_policy.md](docs/dataset_policy.md)
- [docs/training_flow.md](docs/training_flow.md)
- [docs/olmo3_extension.md](docs/olmo3_extension.md)

## Testing

After installing dependencies:

```bash
pytest -q
```

The included tests cover:

- canonical schema validation
- InstructIE conversion behavior
- unified export behavior
- merge deduplication
- split reproducibility
