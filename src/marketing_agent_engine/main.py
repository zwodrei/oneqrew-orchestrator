#!/usr/bin/env python
from __future__ import annotations

import sys
import warnings

from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from marketing_agent_engine.config.settings import settings
from marketing_agent_engine.flows.task_orchestrator_flow import TaskOrchestratorFlow  # noqa: F401


def kickoff() -> None:
    """Flow entry point for AMP — runs the TaskOrchestratorFlow."""
    import json
    import sys

    trigger_payload: dict | None = None
    if len(sys.argv) >= 2:
        try:
            trigger_payload = json.loads(sys.argv[1])
        except (json.JSONDecodeError, IndexError):
            pass

    flow = TaskOrchestratorFlow()
    if trigger_payload:
        flow.kickoff({"crewai_trigger_payload": trigger_payload})
    else:
        flow.kickoff()


def run() -> None:
    """Primary entry point — runs the full orchestration pipeline."""
    from marketing_agent_engine.runtime.orchestrator_runner import OrchestratorRunner

    # Default demo ticket when invoked without arguments
    demo_ticket: dict = {
        "gid": "demo-001",
        "name": "SEO-Optimierung Landingpage Wärmepumpen Q2 2025",
        "notes": (
            "Die Landingpage für Wärmepumpen soll für fünf Ziel-Keywords optimiert werden. "
            "Fokus: Onpage-SEO (H1, Meta, Alt-Texte), Ladezeit, strukturierte Daten."
        ),
        "due_on": "2025-05-01",
        "assignee": None,
        "projects": [{"gid": "proj_shk_q2", "name": "SHK+E Marketing Q2"}],
        "tags": [],
        "custom_fields": [],
        "followers": [],
        "workspace": {"gid": "ws_main"},
        "permalink_url": "https://app.asana.com/0/demo/001",
    }

    runner = OrchestratorRunner()
    result = runner.run(demo_ticket)

    import json
    print("\n" + "=" * 60)
    print("ASANA COMMENT")
    print("=" * 60)
    print(result.comment)

    print("\n" + "=" * 60)
    print("JSON OUTPUT")
    print("=" * 60)
    print(json.dumps(result.json_output, indent=2, default=str))

    print("\n" + "=" * 60)
    print("MCP RESPONSES")
    print("=" * 60)
    print(json.dumps(result.mcp_responses, indent=2, default=str))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(result.summary())


def train() -> None:
    from marketing_agent_engine.crews.analysis_crew.crew import AnalysisCrew
    inputs = {"dry_run": str(settings.dry_run), "model": settings.model}
    AnalysisCrew().crew().train(
        n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
    )


def replay() -> None:
    from marketing_agent_engine.crews.analysis_crew.crew import AnalysisCrew
    AnalysisCrew().crew().replay(task_id=sys.argv[1])


def test() -> None:
    from marketing_agent_engine.crews.analysis_crew.crew import AnalysisCrew
    inputs = {"dry_run": str(settings.dry_run), "model": settings.model}
    AnalysisCrew().crew().test(
        n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
    )


if __name__ == "__main__":
    run()
