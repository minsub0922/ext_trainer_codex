# Dataset Policy

This repository is intended for internal/company usage and treats data licensing as an explicit engineering concern.

## Default vs reference paths

- Default enabled:
  - `InstructIE` as a public seed dataset candidate.
- Reference only:
  - GoLLIE-inspired schemas and prompting ideas.
- Not default:
  - internal company data onboarding.
  - any dataset with unclear or restrictive commercial usage terms.
  - IEPile as a default final-train path.

## Rules encoded in the repo

- Every downloader or onboarding script includes a metadata note with:
  - source
  - expected task types
  - license placeholder
  - whether the path is default enabled
- Raw and processed datasets are isolated in `data/`.
- Dataset docs avoid hiding assumptions. When license review is incomplete, the code marks it as `TODO_VERIFY`.

## GoLLIE usage

GoLLIE is used here as a task-structuring reference for:

- slot-style K/V extraction
- schema-conditioned extraction prompts
- shared structured outputs across entity and relation tasks

It is not a hard runtime dependency of the training pipeline.
