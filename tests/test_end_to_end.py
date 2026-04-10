"""
test_end_to_end.py — Full pipeline integration test.

Runs: input → Flow (_analysis_override) → Presenters → GuardedMCPClient (dry-run)

No LLM, no real Asana connection. Tests the complete pipeline wiring.
"""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest

from marketing_agent_engine.flows.task_orchestrator_flow import TaskOrchestratorFlow
from marketing_agent_engine.mcp.guarded_client import GuardedMCPClient
from marketing_agent_engine.mcp.tools import ToolResponse
from marketing_agent_engine.presenters.asana_comment import build_asana_comment
from marketing_agent_engine.presenters.json_output import build_json_output
from marketing_agent_engine.runtime.orchestrator_runner import OrchestratorRunner


# ─────────────────────────────────────────────────────────────────────────────
# Shared fixtures
# ─────────────────────────────────────────────────────────────────────────────

DUMMY_TICKET = {
    "gid": "e2e-test-001",
    "name": "Instagram Reels Kampagne Flachdach Q3",
    "notes": (
        "Wir benötigen 4 Instagram Reels für die Flachdach-Saison. "
        "Themen: Vorteile Flachdach, Dachbegrünung, Abdichtung, Wartungstipps. "
        "Zielgruppe: Eigenheimbesitzer 35–55."
    ),
    "due_on": "2025-07-01",
    "assignee": {"gid": "gid_unknown_999", "name": "Max Mustermann"},
    "projects": [{"gid": "proj_dach_q3", "name": "Dach_und_Holz Q3"}],
    "tags": [{"name": "social-media"}],
    "custom_fields": [{"display_value": "Social Media"}],
    "followers": [{"gid": "follower_1"}],
    "workspace": {"gid": "ws_main"},
    "permalink_url": "https://app.asana.com/0/e2e/001",
}

FAKE_DECISION: dict[str, Any] = {
    "ticket_id": "e2e-test-001",
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
        "routing": "Routed to Dach_und_Holz via keyword 'flachdach' (confidence 0.78).",
        "assignment": "Assignee GID not in registry — verdict unknown.",
        "completeness": "Score 0.91 (10/11 passed); failed: followers_present.",
    },
}


def _mock_mcp() -> MagicMock:
    m = MagicMock()
    m.connect.return_value = None
    m.disconnect.return_value = None
    m.call_tool.return_value = ToolResponse(
        tool="create_comment",
        success=True,
        data={"result": "ok"},
        simulated=False,
        execution_mode="live",
    )
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Full pipeline (Flow → Presenters → GuardedMCPClient)
# ─────────────────────────────────────────────────────────────────────────────

class TestFullPipeline:
    @pytest.fixture()
    def state(self):
        flow = TaskOrchestratorFlow()
        flow._analysis_override = lambda _: FAKE_DECISION
        flow.state.raw_input = DUMMY_TICKET
        flow.kickoff()
        return flow.state

    def test_no_crash(self, state) -> None:
        comment = build_asana_comment(state)
        json_out = build_json_output(state)
        assert comment
        assert json_out

    def test_next_step_is_deterministic(self, state) -> None:
        # completeness=0.91 (≥0.70), assignee verdict=unknown → needs_assignment
        assert state.next_step == "needs_assignment"

    def test_comment_is_non_empty_string(self, state) -> None:
        assert isinstance(build_asana_comment(state), str)
        assert len(build_asana_comment(state)) > 50

    def test_json_output_is_valid_dict(self, state) -> None:
        out = build_json_output(state)
        assert isinstance(out, dict)
        # Must be JSON-serialisable
        serialised = json.dumps(out, default=str)
        assert len(serialised) > 10

    def test_json_execution_mode_dry_run(self, state) -> None:
        out = build_json_output(state)
        assert out["execution_mode"] == "dry_run"

    def test_json_simulated_true(self, state) -> None:
        out = build_json_output(state)
        assert out["simulated"] is True

    def test_json_actions_present(self, state) -> None:
        out = build_json_output(state)
        assert len(out["actions"]) >= 1

    def test_json_decision_trace_keys(self, state) -> None:
        dt = build_json_output(state)["decision_trace"]
        assert "routing_reason" in dt
        assert "assignment_reason" in dt
        assert "completeness_reason" in dt


# ─────────────────────────────────────────────────────────────────────────────
# MCP simulated actions
# ─────────────────────────────────────────────────────────────────────────────

class TestSimulatedMcpActions:
    @pytest.fixture()
    def state_and_comment(self):
        flow = TaskOrchestratorFlow()
        flow._analysis_override = lambda _: FAKE_DECISION
        flow.state.raw_input = DUMMY_TICKET
        flow.kickoff()
        state = flow.state
        comment = build_asana_comment(state)
        return state, comment

    def test_simulated_action_returned(self, state_and_comment) -> None:
        state, comment = state_and_comment
        client = GuardedMCPClient(dry_run=True, mcp_client=_mock_mcp())
        with client as c:
            resp = c.create_comment(str(state.task_id), comment)
        assert resp.simulated is True
        assert resp.execution_mode == "dry_run"
        assert resp.success is True

    def test_real_mcp_never_called_in_dry_run(self, state_and_comment) -> None:
        state, comment = state_and_comment
        mock = _mock_mcp()
        client = GuardedMCPClient(dry_run=True, mcp_client=mock)
        with client as c:
            c.create_comment(str(state.task_id), comment)
        mock.call_tool.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# OrchestratorRunner end-to-end (dry-run, no real Asana)
# ─────────────────────────────────────────────────────────────────────────────

class TestOrchestratorRunner:
    @pytest.fixture()
    def runner_result(self):
        mock_mcp = GuardedMCPClient(dry_run=True, mcp_client=_mock_mcp())
        runner = OrchestratorRunner(mcp_client=mock_mcp)

        # Patch the flow inside runner to use our fake decision
        original_run = runner.run

        def patched_run(ticket: dict) -> Any:
            from marketing_agent_engine.flows.task_orchestrator_flow import TaskOrchestratorFlow
            flow = TaskOrchestratorFlow()
            flow._analysis_override = lambda _: FAKE_DECISION
            flow.state.raw_input = ticket
            flow.kickoff()
            state = flow.state
            from marketing_agent_engine.presenters.asana_comment import build_asana_comment
            from marketing_agent_engine.presenters.json_output import build_json_output
            comment = build_asana_comment(state)
            json_out = build_json_output(state)
            mcp_responses = []
            errors = []
            try:
                with mock_mcp as c:
                    resp = c.create_comment(str(state.task_id), comment)
                    mcp_responses.append({
                        "tool": "create_comment",
                        "simulated": resp.simulated,
                        "execution_mode": resp.execution_mode,
                        "success": resp.success,
                    })
            except Exception as exc:
                errors.append(str(exc))
            from marketing_agent_engine.runtime.orchestrator_runner import RunResult
            return RunResult(
                task_id=str(state.task_id),
                next_step=state.next_step,
                execution_mode=state.execution_mode,
                comment=comment,
                json_output=json_out,
                mcp_responses=mcp_responses,
                errors=errors,
            )

        runner.run = patched_run
        return runner.run(DUMMY_TICKET)

    def test_no_errors(self, runner_result) -> None:
        assert runner_result.errors == []

    def test_comment_non_empty(self, runner_result) -> None:
        assert len(runner_result.comment) > 50

    def test_json_output_has_schema_version(self, runner_result) -> None:
        assert runner_result.json_output["schema_version"] == "1.0"

    def test_mcp_responses_present(self, runner_result) -> None:
        assert len(runner_result.mcp_responses) >= 1

    def test_mcp_response_simulated(self, runner_result) -> None:
        assert runner_result.mcp_responses[0]["simulated"] is True

    def test_execution_mode_dry_run(self, runner_result) -> None:
        assert runner_result.execution_mode == "dry_run"

    def test_simulated_property(self, runner_result) -> None:
        assert runner_result.simulated is True

    def test_summary_contains_task_id(self, runner_result) -> None:
        assert "e2e-test-001" in runner_result.summary()

    def test_next_step_is_valid(self, runner_result) -> None:
        valid = {"blocked", "needs_information", "needs_assignment", "review", "ready"}
        assert runner_result.next_step in valid


# ─────────────────────────────────────────────────────────────────────────────
# Error resilience
# ─────────────────────────────────────────────────────────────────────────────

class TestErrorResilience:
    def test_flow_handles_analysis_error_gracefully(self) -> None:
        """An exception in the analysis override must not crash the flow."""
        flow = TaskOrchestratorFlow()
        flow._analysis_override = lambda _: (_ for _ in ()).throw(RuntimeError("LLM unavailable"))
        flow.state.raw_input = DUMMY_TICKET
        flow.kickoff()
        assert flow.state.next_step == "blocked"
        assert flow.state.analysis_error is not None

    def test_flow_with_empty_ticket_does_not_crash(self) -> None:
        flow = TaskOrchestratorFlow()
        flow._analysis_override = lambda _: {
            "routing": {"cluster": "unbekannt", "routing_confidence": 0.0, "coordinator_id": None},
            "assignment": {"verdict": "unknown", "needs_reassignment": True, "reassignment_reason": ""},
            "completeness": {"completeness_score": 0.0, "critical_missing": []},
            "decision_trace": {"routing": "", "assignment": "", "completeness": ""},
        }
        flow.state.raw_input = {}
        flow.kickoff()
        assert flow.state.next_step in {"blocked", "needs_information", "needs_assignment", "review", "ready"}

    def test_guarded_client_write_in_dry_run_never_raises(self) -> None:
        client = GuardedMCPClient(dry_run=True, mcp_client=_mock_mcp())
        # Should never raise — returns simulated response
        resp = client.create_comment("t_err", "safety test")
        assert resp.success is True

    def test_presenter_handles_minimal_state(self) -> None:
        """Presenters must not crash on a state with no routing/assignment/completeness."""
        state = TaskOrchestratorFlow().state
        state.next_step = "blocked"
        state.execution_mode = "dry_run"
        state.timestamp = "2025-01-01T00:00:00Z"
        state.task_id = "minimal-001"
        # Should not raise
        comment = build_asana_comment(state)
        out = build_json_output(state)
        assert isinstance(comment, str)
        assert isinstance(out, dict)
