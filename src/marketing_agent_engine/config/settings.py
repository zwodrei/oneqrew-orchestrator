from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


class Settings:
    dry_run: bool = _parse_bool(os.getenv("DRY_RUN", "true"))
    model: str = os.getenv("MODEL", "openai/gpt-4o-mini")
    crewai_api_key: str = os.getenv("CREWAI_API_KEY", "")


settings = Settings()
