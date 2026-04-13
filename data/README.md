# Data

This repository treats dataset handling as license-sensitive and internal-first.

## Directory roles

- `raw/`: untouched downloads or manually staged source files.
- `interim/`: partially normalized artifacts, usually dataset-specific.
- `processed/`: canonical JSONL datasets, merged datasets, splits, and LLaMA-Factory exports.
- `metadata/`: registry and dataset policy records.

## Commit policy

- Commit metadata, configs, and tiny synthetic examples.
- Do not commit internal source documents, large raw public downloads, model weights, or sensitive processed outputs.
- Keep dataset usage isolated and explicit. Every downloader writes or expects a short metadata note including source, task types, license, and whether the path is default enabled.
