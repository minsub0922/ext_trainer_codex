# Scripts

All scripts are small CLIs around the modules in `src/`. The canonical schema is always the primary representation. LLaMA-Factory format is only generated downstream.

## Download

- `scripts/download/download_instructie.py`
  Purpose: stage InstructIE raw files and write dataset metadata notes.
  Args: `--output`, `--source-url`, `--dataset-id`, `--config-name`, `--split`, `--dry-run`
  Example: `python scripts/download/download_instructie.py --dataset-id zjunlp/InstructIE`
  Output: note file and optionally raw asset under `data/raw/instructie/`
  Note: Hugging Face dataset page URLs are detected and downloaded through the `datasets` library path.

- `scripts/download/download_reference_gollie_assets.py`
  Purpose: create a reference-only note for GoLLIE-inspired assets.
  Example: `python scripts/download/download_reference_gollie_assets.py`

- `scripts/download/download_internal_template.py`
  Purpose: create an internal dataset onboarding note.

## Preprocess

- `scripts/preprocess/normalize_instructie.py`
  Purpose: convert raw InstructIE JSON/JSONL into canonical JSONL.
  Example: `python scripts/preprocess/normalize_instructie.py --input data/raw/instructie/train.jsonl --output data/processed/instructie_canonical.jsonl --split train`

- `scripts/preprocess/build_internal_kv_template.py`
  Purpose: generate annotation-ready K/V skeletons from CSV/JSONL.
  Example: `python scripts/preprocess/build_internal_kv_template.py --input internal.csv --output data/processed/internal_kv_template.jsonl --config configs/datasets/internal_kv_example.yaml`

- `scripts/preprocess/unify_ie_datasets.py`
  Purpose: merge multiple canonical datasets with deduplication and task filtering.
  Example: `python scripts/preprocess/unify_ie_datasets.py --input data/processed/instructie_canonical.jsonl data/processed/internal_kv_template.jsonl --output data/processed/unified.jsonl --stats-output data/processed/unified_stats.json`

- `scripts/preprocess/validate_canonical_dataset.py`
  Purpose: validate canonical JSONL rows before export or training.

## Export

- `scripts/export/export_train_dev_test.py`
  Purpose: assign or materialize train/dev/test files.
  Example: `python scripts/export/export_train_dev_test.py --input data/processed/unified.jsonl --output-dir data/processed/splits --seed 42 --overwrite`

- `scripts/export/export_to_llamafactory.py`
  Purpose: convert canonical JSONL into LLaMA-Factory instruction JSONL and `dataset_info.json`.
  Args: `--input`, `--output`, `--mode`, `--dataset-name`, `--overwrite`
  Modes: `kv`, `entity`, `relation`, `unified`

## Train

- `scripts/train/run_sft_qwen3.sh`
- `scripts/train/run_sft_qwen35.sh`
- `scripts/train/run_sft_olmo3_poc.sh`
- `scripts/train/run_eval_qwen3.sh`
- `scripts/train/run_infer_qwen3.sh`
- `scripts/train/merge_lora_qwen3.sh`

These scripts print the resolved config, accept environment-variable overrides, and fail loudly when required files are missing.

## Utils

- `scripts/utils/env_check.py`: import sanity checks.
- `scripts/utils/print_dataset_stats.py`: canonical dataset statistics.
