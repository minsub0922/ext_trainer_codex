# Training Flow

## End-to-end path

1. Prepare environment.
2. Download or stage InstructIE.
3. Normalize InstructIE into canonical JSONL.
4. Build internal K/V annotation templates if needed.
5. Merge canonical datasets.
6. Split into train/dev/test.
7. Export to LLaMA-Factory format.
8. Run LoRA SFT.
9. Run eval or inference.
10. Optionally merge LoRA weights.

## Example commands

```bash
python scripts/download/download_instructie.py --dry-run
python scripts/preprocess/normalize_instructie.py \
  --input data/raw/instructie/sample.json \
  --output data/processed/instructie_canonical.jsonl \
  --split train

python scripts/preprocess/build_internal_kv_template.py \
  --input internal.csv \
  --output data/processed/internal_kv_template.jsonl \
  --config configs/datasets/internal_kv_example.yaml

python scripts/preprocess/unify_ie_datasets.py \
  --input data/processed/instructie_canonical.jsonl data/processed/internal_kv_template.jsonl \
  --output data/processed/unified.jsonl \
  --stats-output data/processed/unified_stats.json

python scripts/export/export_train_dev_test.py \
  --input data/processed/unified.jsonl \
  --output-dir data/processed/splits \
  --seed 42 --overwrite

python scripts/export/export_to_llamafactory.py \
  --input data/processed/unified.jsonl \
  --output data/processed/llamafactory \
  --mode unified \
  --dataset-name internal_ie_unified \
  --overwrite

bash scripts/train/run_sft_qwen3.sh
```

## Assumptions

- `llamafactory-cli` is installed and reachable or `LLAMA_FACTORY_CLI` is set.
- Config YAMLs are used as the stable operator interface for training changes.
