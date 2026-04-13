# OLMo3 Extension PoC

This repository does not make OLMo3 the default path today. The goal is to keep future adoption cheap.

## What is already reusable

- canonical schema
- dataset normalization
- unified merge and split
- LLaMA-Factory export
- dataset registry generation
- train script shape

## What remains model-specific

- model checkpoint choice
- prompt template compatibility
- tokenizer quirks and special token handling
- LoRA target module validation
- empirical hyperparameter tuning

## PoC components

- `configs/models/olmo3_poc.yaml`
- `configs/sft/olmo3_poc_sft.yaml`
- `src/models/olmo.py`
- `src/olmo3_poc/adapter.py`
- `scripts/train/run_sft_olmo3_poc.sh`

## Limitations

- The current config uses an OLMo-family placeholder path as a compatibility sketch.
- This is not presented as productionized.
- Before real OLMo3 work, validate tokenizer behavior, chat template mapping, and target modules against the exact checkpoint.
