#!/usr/bin/env bash
set -euo pipefail

MODEL_CONFIG="${MODEL_CONFIG:-configs/models/qwen3_5_0_8b.yaml}"
SFT_CONFIG="${SFT_CONFIG:-configs/sft/qwen3_5_lora_sft.yaml}"
RUNTIME_CONFIG="${RUNTIME_CONFIG:-/tmp/qwen35_runtime_sft.yaml}"

[[ -f "$MODEL_CONFIG" ]] || { echo "Missing model config: $MODEL_CONFIG" >&2; exit 1; }
[[ -f "$SFT_CONFIG" ]] || { echo "Missing SFT config: $SFT_CONFIG" >&2; exit 1; }

echo "Model config: $MODEL_CONFIG"
echo "SFT config:   $SFT_CONFIG"
python -c "from src.training.config_builder import load_config, render_training_config, save_training_config; cfg=render_training_config(load_config('$MODEL_CONFIG'), load_config('$SFT_CONFIG')); save_training_config('$RUNTIME_CONFIG', cfg)"
python -c "from src.training.llamafactory_runner import print_config; print_config('$RUNTIME_CONFIG')"
python -c "from src.training.llamafactory_runner import run_train; raise SystemExit(run_train('$RUNTIME_CONFIG', dry_run=False))"
