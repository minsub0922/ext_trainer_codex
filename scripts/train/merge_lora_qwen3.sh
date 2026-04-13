#!/usr/bin/env bash
set -euo pipefail

ADAPTER_PATH="${ADAPTER_PATH:-outputs/qwen3-0.6b-lora}"
EXPORT_DIR="${EXPORT_DIR:-outputs/qwen3-0.6b-merged}"
LLAMA_FACTORY_CLI="${LLAMA_FACTORY_CLI:-llamafactory-cli}"

[[ -d "$ADAPTER_PATH" ]] || { echo "Missing adapter directory: $ADAPTER_PATH" >&2; exit 1; }
mkdir -p "$EXPORT_DIR"
echo "Adapter path: $ADAPTER_PATH"
echo "Export dir:   $EXPORT_DIR"
echo "Command: $LLAMA_FACTORY_CLI export --adapter_name_or_path $ADAPTER_PATH --export_dir $EXPORT_DIR"
"$LLAMA_FACTORY_CLI" export --adapter_name_or_path "$ADAPTER_PATH" --export_dir "$EXPORT_DIR"
