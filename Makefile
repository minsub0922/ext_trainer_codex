PYTHON ?= python3

.PHONY: env-check test stats example-export

env-check:
	$(PYTHON) scripts/utils/env_check.py

test:
	pytest -q

stats:
	$(PYTHON) scripts/utils/print_dataset_stats.py --input data/processed/unified.jsonl

example-export:
	$(PYTHON) scripts/export/export_to_llamafactory.py \
		--input data/processed/unified.jsonl \
		--output data/processed/llamafactory \
		--mode unified \
		--overwrite
