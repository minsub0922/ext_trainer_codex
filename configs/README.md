# Configs

This directory is config-first on purpose. The canonical schema is the source of truth, while these YAML files control dataset preparation and LLaMA-Factory execution details.

## Layout

- `datasets/`: dataset source and onboarding examples.
- `models/`: model-family defaults such as `model_name_or_path`, prompt template, and sequence length.
- `sft/`: train-time defaults layered on top of a model config.

## Override pattern

1. Pick a model config.
2. Pick an SFT config.
3. Override any runtime values in shell, copied YAML, or a generated merged YAML.

Typical override targets:

- `model_name_or_path`
- `template`
- `dataset`
- `dataset_dir`
- `output_dir`
- `finetuning_type`
- `bf16` / `fp16`
- `per_device_train_batch_size`
- `gradient_accumulation_steps`
- `learning_rate`
- `num_train_epochs`
- `cutoff_len`
- `eval_strategy`
- `save_strategy`
