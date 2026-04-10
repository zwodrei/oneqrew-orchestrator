from __future__ import annotations

import os
from crewai import LLM


# ─── Hard block: Anthropic ─────────────────────────────────────────────────
def _fail_if_anthropic() -> None:
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    zhipu_key = os.getenv("ZHIPUAI_API_KEY", "")

    if anthropic_key and not openai_key and not zhipu_key:
        raise RuntimeError(
            "HARD REQUIREMENT VIOLATION: Anthropic is NOT allowed. "
            "Set OPENAI_API_KEY or ZHIPUAI_API_KEY instead."
        )


# ─── LLM factory ───────────────────────────────────────────────────────────
def get_default_llm() -> LLM:
    _fail_if_anthropic()

    model = os.getenv("MODEL", "openai/gpt-4o-mini")

    # Block Anthropic model strings
    if "anthropic" in model.lower() or "claude" in model.lower():
        raise RuntimeError(
            f"HARD REQUIREMENT VIOLATION: Model '{model}' is Anthropic-based. "
            "Use 'openai/gpt-4o-mini' or 'zhipuai/glm-4-5'."
        )

    return LLM(
        model=model,
        temperature=0.2,
    )
