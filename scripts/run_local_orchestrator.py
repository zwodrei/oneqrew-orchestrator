#!/usr/bin/env python
"""
scripts/run_local_orchestrator.py

End-to-end local smoke test for the Marketing Agent Engine.
Uses TaskOrchestratorFlow._analysis_override to bypass the real AnalysisCrew
(no LLM call needed). The full pipeline runs:

  Flow → Presenters → GuardedMCPClient (dry-run, simulated)

Usage:
    cd oneqrew
    uv run --prerelease=allow python scripts/run_local_orchestrator.py
"""
from __future__ import annotations

import json
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
for noisy in ("httpx", "openai", "crewai", "litellm"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

logger = logging.getLogger("run_local_orchestrator")

# ---------------------------------------------------------------------------
# Dummy ticket
# ---------------------------------------------------------------------------

DUMMY_TICKET = {
    "gid": "test-123",
    "name": "Instagram Reels Kampagne Flachdach Q3",
    "notes": (
        "Wir brauchen 4 Instagram Reels für die Flachdach-Saison. "
        "Themen: Vorteile Flachdach, Dachbegrünung, Abdichtung, Wartungstipps. "
        "Zielgruppe: Eigenheimbesitzer 35-55."
    ),
    "due_on": "2025-07-01",
    "assignee": {"gid": "gid_unknown_999", "name": "Max Mustermann"},
    "projects": [{"gid": "proj_dach_q3", "name": "Dach_und_Holz Q3"}],
    "tags": [{"name": "social-media"}],
    "custom_fields": [{"display_value": "Social Media"}],
    "followers": [{"gid": "follower_1"}],
    "workspace": {"gid": "ws_main"},
    "permalink_url": "https://app.asana.com/0/test/123",
}

# Pre-built decision — mirrors what AnalysisCrew would return
FAKE_DECISION = {
    "ticket_id": "test-123",
    "dry_run": True,
    "execution_mode": "dry_run",
    "model_used": "openai/gpt-4.1",
    "timestamp": "2025-04-15T10:00:00Z",
    "routing": {
        "cluster": "Dach_und_Holz",
        "business_unit_slug": "dach_flachdach",
        "routing_confidence": 0.78,
        "coordinator_id": "emp_004",
    },
    "assignment": {
        "verdict": "unknown",
        "assignment_confidence": 0.0,
        "needs_reassignment": True,
        "reassignment_reason": "Assignee 'Max Mustermann' not found in employee registry.",
        "top_recommendation": {
            "employee_id": "emp_006",
            "display_name": "Felix Hoffmann",
            "confidence": 1.0,
            "matched_skills": ["social_media", "design", "content_creation"],
        },
    },
    "completeness": {
        "completeness_score": 0.91,
        "passed": True,
        "missing_count": 1,
        "critical_missing": ["followers_present"],
    },
    "decision_trace": {
        "routing": "Routed to Dach_und_Holz via keyword 'flachdach' (confidence 0.78); coordinator emp_004.",
        "assignment": "Assignee GID not in registry — verdict unknown; top rec: Felix Hoffmann (100%).",
        "completeness": "Score 0.91 (10/11 passed); failed: followers_present.",
    },
    "overall_status": "needs_attention",
}


def main() -> None:
    from marketing_agent_engine.flows.task_orchestrator_flow import TaskOrchestratorFlow
    from marketing_agent_engine.mcp.guarded_client import GuardedMCPClient
    from marketing_agent_engine.runtime.orchestrator_runner import OrchestratorRunner, RunResult, _log_state
    from marketing_agent_engine.presenters.asana_comment import build_asana_comment
    from marketing_agent_engine.presenters.json_output import build_json_output

    # Inject fake decision via the official test hook — no LLM, no metaclass issues
    flow = TaskOrchestratorFlow()
    flow._analysis_override = lambda ticket: FAKE_DECISION
    flow.state.raw_input = DUMMY_TICKET
    flow.kickoff()
    state = flow.state

    _log_state(state)

    comment = build_asana_comment(state)
    json_out = build_json_output(state)

    # Simulate MCP call via GuardedMCPClient (dry_run=True)
    mcp_client = GuardedMCPClient(dry_run=True)
    mcp_responses = []
    if state.next_step:
        with mcp_client as client:
            resp = client.create_comment(
                task_id=str(state.task_id),
                text=comment,
                is_pinned=(state.next_step in ("blocked", "needs_assignment")),
            )
            mcp_responses.append({
                "tool": "create_comment",
                "task_id": str(state.task_id),
                "next_step": state.next_step,
                "simulated": resp.simulated,
                "execution_mode": resp.execution_mode,
                "success": resp.success,
                "payload_preview": (comment[:120] + "…") if len(comment) > 120 else comment,
            })

    sep = "=" * 64

    print(f"\n{sep}")
    print("1. ASANA COMMENT")
    print(sep)
    print(comment)

    print(f"\n{sep}")
    print("2. JSON OUTPUT")
    print(sep)
    print(json.dumps(json_out, indent=2, default=str))

    print(f"\n{sep}")
    print("3. SIMULATED MCP CALLS")
    print(sep)
    print(json.dumps(mcp_responses, indent=2, default=str))

    print(f"\n{sep}")
    print("SUMMARY")
    print(sep)
    print(f"task_id={state.task_id} | next_step={state.next_step} | "
          f"execution_mode={state.execution_mode} | mcp_calls={len(mcp_responses)}")


if __name__ == "__main__":
    main()
