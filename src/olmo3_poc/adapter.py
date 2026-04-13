"""Simple model-family adapter abstraction for future OLMo3 support."""

from __future__ import annotations

from dataclasses import dataclass

from src.models.model_registry import get_model_spec


@dataclass(slots=True)
class ModelFamilyAdapter:
    family: str
    default_template: str
    tokenizer_quirks: str
    recommended_prompt_style: str
    training_overrides: dict


def build_olmo3_adapter() -> ModelFamilyAdapter:
    spec = get_model_spec("olmo3-poc")
    return ModelFamilyAdapter(
        family=spec.family,
        default_template=spec.template,
        tokenizer_quirks=spec.tokenizer_quirks,
        recommended_prompt_style=spec.recommended_prompt_style,
        training_overrides={"bf16": True, "cutoff_len": spec.max_length, "lora_target": "all"},
    )
