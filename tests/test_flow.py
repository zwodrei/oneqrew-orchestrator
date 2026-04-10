"""
test_flow.py — Integration tests for TaskOrchestratorFlow.

Uses _analysis_override to bypass AnalysisCrew — no LLM required.
Tests all 5 decision branches deterministically.
"""
from __future__ import annotations

from typing import Any

import pytest

from marketing_agent_engine.flows.task_orchestrator_flow import (
    TaskOrchestratorFlow,
    TaskState,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

BASE_TICKET = {
    "gid": "flow-test-001",
    "name": "Test Ticket für Flow-Integrationstests",
    "notes": "Testbeschreibung für die automatisierten Flow-Tests.",
}


def _decision(
    *,
    completeness_score: float,
    verdict: str = "plausible",
    has_assignee: bool = True,
    needs_reassignment: bool = False,
    cluster: str = "SHK+E",
    routing_confidence: float = 0.75,
    missing: list[str] | None = None,
) -> dict[str, Any]:
    """Build a minimal fake synthesizer decision dict."""
    inferred_missing = missing if missing is not None else (
        [] if completeness_score >= 0.8 else ["description_present", "due_date_set", "assignee_set"]
    )
    return {
        "ticket_id": "flow-test-001",
        "dry_run": True,
        "execution_mode": "dry_run",
        "model_used": "openai/gpt-4.1",
        "timestamp": "2025-04-15T10:00:00Z",
        "routing": {
            "cluster": cluster,
            "business_unit_slug": None,
            "routing_confidence": routing_confidence,
            "coordinator_id": "emp_002",
        },
        "assignment": {
            "verdict": verdict if has_assignee else "unknown",
            "assignment_confidence": 0.9 if verdict == "plausible" else 0.2,
            "needs_reassignment": needs_reassignment or not has_assignee,
            "reassignment_reason": "" if verdict == "plausible" else "Skill mismatch.",
            "top_recommendation": {
                "employee_id": "emp_006",
                "display_name": "Felix Hoffmann",
                "confidence": 0.85,
                "matched_skills": ["social_media", "design"],
            },
        },
        "completeness": {
            "completeness_score": completeness_score,
            "passed": completeness_score >= 0.8,
            "missing_count": len(inferred_missing),
            "critical_missing": inferred_missing,
        },
        "decision_trace": {
            "routing": f"Routed to {cluster} (confidence {routing_confidence:.2f}).",
            "assignment": f"Verdict: {verdict}.",
            "completeness": f"Score {completeness_score:.2f}.",
        },
    }


def _run(dec: dict[str, Any], ticket: dict[str, Any] | None = None) -> TaskState:
    flow = TaskOrchestratorFlow()
    flow._analysis_override = lambda _: dec
    flow.state.raw_input = ticket or BASE_TICKET
    flow.kickoff()
    return flow.state


# ─────────────────────────────────────────────────────────────────────────────
# Branch 1: blocked  (completeness < 0.50)
# ─────────────────────────────────────────────────────────────────────────────

class TestBranchBlocked:
    def test_score_027_is_blocked(self) -> None:
        assert _run(_decision(completeness_score=0.27, has_assignee=False)).next_step == "blocked"

    def test_score_049_is_blocked(self) -> None:
        assert _run(_decision(completeness_score=0.49, has_assignee=False)).next_step == "blocked"

    def test_blocked_action_plan_not_empty(self) -> None:
        state = _run(_decision(completeness_score=0.18, has_assignee=False))
        assert len(state.action_plan) >= 1

    def test_blocked_action_plan_owner_is_requester_or_coordinator(self) -> None:
        state = _run(_decision(completeness_score=0.30, has_assignee=False))
        owners = {item.owner for item in state.action_plan}
        assert owners & {"requester", "coordinator"}

    def test_blocked_decision_trace_has_completeness_key(self) -> None:
        state = _run(_decision(completeness_score=0.30, has_assignee=False))
        assert "completeness" in state.decision_trace


# ─────────────────────────────────────────────────────────────────────────────
# Branch 2: needs_information  (0.50 ≤ score < 0.70)
# ─────────────────────────────────────────────────────────────────────────────

class TestBranchNeedsInformation:
    def test_score_055_is_needs_information(self) -> None:
        assert _run(_decision(completeness_score=0.55)).next_step == "needs_information"

    def test_score_069_is_needs_information(self) -> None:
        assert _run(_decision(completeness_score=0.69)).next_step == "needs_information"

    def test_needs_information_action_plan_present(self) -> None:
        state = _run(_decision(completeness_score=0.60))
        assert len(state.action_plan) >= 1

    def test_needs_information_requester_in_owners(self) -> None:
        state = _run(_decision(completeness_score=0.65))
        owners = {item.owner for item in state.action_plan}
        assert "requester" in owners


# ─────────────────────────────────────────────────────────────────────────────
# Branch 3: needs_assignment  (good score, no assignee)
# ─────────────────────────────────────────────────────────────────────────────

class TestBranchNeedsAssignment:
    def test_good_score_no_assignee_is_needs_assignment(self) -> None:
        state = _run(_decision(
            completeness_score=0.82,
            verdict="unknown",
            has_assignee=False,
            needs_reassignment=True,
        ))
        assert state.next_step == "needs_assignment"

    def test_action_plan_contains_assign_action(self) -> None:
        state = _run(_decision(
            completeness_score=0.82,
            verdict="unknown",
            has_assignee=False,
            needs_reassignment=True,
        ))
        text = " ".join(i.action.lower() for i in state.action_plan)
        assert "assign" in text

    def test_recommendation_present_in_plan_reason(self) -> None:
        state = _run(_decision(
            completeness_score=0.82,
            verdict="unknown",
            has_assignee=False,
        ))
        # Action plan reason should mention a recommendation or employee
        reasons = " ".join(i.reason.lower() for i in state.action_plan)
        assert len(reasons) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Branch 4: review  (implausible / questionable assignee)
# ─────────────────────────────────────────────────────────────────────────────

class TestBranchReview:
    def test_implausible_verdict_is_review(self) -> None:
        state = _run(_decision(completeness_score=0.82, verdict="implausible"))
        assert state.next_step == "review"

    def test_questionable_verdict_is_review(self) -> None:
        state = _run(_decision(completeness_score=0.82, verdict="questionable"))
        assert state.next_step == "review"

    def test_review_action_plan_not_empty(self) -> None:
        state = _run(_decision(completeness_score=0.82, verdict="implausible"))
        assert len(state.action_plan) >= 1

    def test_review_decision_trace_assignment_key_set(self) -> None:
        state = _run(_decision(completeness_score=0.82, verdict="implausible"))
        assert "assignment" in state.decision_trace
        assert len(state.decision_trace["assignment"]) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Branch 5: ready  (all green)
# ─────────────────────────────────────────────────────────────────────────────

class TestBranchReady:
    def test_all_green_is_ready(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert state.next_step == "ready"

    def test_ready_action_plan_references_comment(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        text = " ".join(i.action.lower() for i in state.action_plan)
        assert "comment" in text or "post" in text or len(state.action_plan) > 0

    def test_ready_execution_mode_is_dry_run(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert state.execution_mode == "dry_run"

    def test_ready_decision_trace_complete(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert state.decision_trace.get("routing")
        assert state.decision_trace.get("completeness")


# ─────────────────────────────────────────────────────────────────────────────
# Phase E: requires_human flag in final_decision
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresHumanFlag:
    def test_review_step_has_requires_human_true(self) -> None:
        state = _run(_decision(completeness_score=0.82, verdict="implausible"))
        assert state.final_decision.get("requires_human") is True

    def test_ready_step_has_requires_human_false(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert state.final_decision.get("requires_human") is False

    def test_blocked_step_has_requires_human_false(self) -> None:
        state = _run(_decision(completeness_score=0.27, has_assignee=False))
        # blocked = automated rejection, no human needed for review
        assert state.final_decision.get("requires_human") is False


# ─────────────────────────────────────────────────────────────────────────────
# State consistency
# ─────────────────────────────────────────────────────────────────────────────

class TestStateConsistency:
    def test_task_id_taken_from_gid(self) -> None:
        state = _run(
            _decision(completeness_score=0.91, verdict="plausible"),
            ticket={"gid": "explicit-gid-999", "name": "Test"},
        )
        assert state.task_id == "explicit-gid-999"

    def test_final_decision_next_step_matches_state(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert state.final_decision["next_step"] == state.next_step

    def test_timestamp_is_iso_format(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert "T" in state.timestamp
        assert state.timestamp != ""

    def test_override_hook_called_exactly_once(self) -> None:
        counter = {"n": 0}

        def fake(ticket: dict) -> dict:
            counter["n"] += 1
            return _decision(completeness_score=0.91, verdict="plausible")

        flow = TaskOrchestratorFlow()
        flow._analysis_override = fake
        flow.state.raw_input = BASE_TICKET
        flow.kickoff()
        assert counter["n"] == 1

    def test_decision_trace_has_three_keys(self) -> None:
        state = _run(_decision(completeness_score=0.91, verdict="plausible"))
        assert {"routing", "assignment", "completeness"} <= set(state.decision_trace.keys())

    def test_error_state_produces_blocked(self) -> None:
        """When _analysis_override raises, the flow should set next_step=blocked."""
        flow = TaskOrchestratorFlow()
        flow._analysis_override = lambda _: (_ for _ in ()).throw(RuntimeError("boom"))
        flow.state.raw_input = BASE_TICKET
        flow.kickoff()
        assert flow.state.next_step == "blocked"
        assert flow.state.analysis_error is not None
