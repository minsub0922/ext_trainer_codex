#!/usr/bin/env bash
set -euo pipefail

MODEL_CONFIG="${MODEL_CONFIG:-configs/models/qwen3_0_6b.yaml}"
CONFIG_PATH="${CONFIG_PATH:-configs/sft/qwen3_lora_sft.yaml}"
RUNTIME_CONFIG="${RUNTIME_CONFIG:-/tmp/qwen3_infer_runtime.yaml}"
[[ -f "$MODEL_CONFIG" ]] || { echo "Missing model config: $MODEL_CONFIG" >&2; exit 1; }
[[ -f "$CONFIG_PATH" ]] || { echo "Missing inference config: $CONFIG_PATH" >&2; exit 1; }
echo "Model config:     $MODEL_CONFIG"
echo "Inference config: $CONFIG_PATH"
python -c "from src.training.config_builder import load_config, render_training_config, save_training_config; cfg=render_training_config(load_config('$MODEL_CONFIG'), load_config('$CONFIG_PATH'), {'do_train': False, 'infer_backend': 'huggingface'}); save_training_config('$RUNTIME_CONFIG', cfg)"
python -c "from src.training.llamafactory_runner import print_config; print_config('$RUNTIME_CONFIG')"
python -c "from src.training.inference_runner import run_api_chat; raise SystemExit(run_api_chat('$RUNTIME_CONFIG', dry_run=False))"
