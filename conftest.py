"""
Local pytest configuration for marketing_agent_engine.

Kept minimal — this file exists to stop pytest from traversing up
to the workspace-level conftest.py (which requires vcrpy).
"""
from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def _force_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """All tests run with DRY_RUN=true unless they override it explicitly."""
    monkeypatch.setenv("DRY_RUN", "true")
    # Reload settings so the monkeypatched value is picked up
    import importlib
    import marketing_agent_engine.config.settings as _s
    _s.settings.dry_run = True
