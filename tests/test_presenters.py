"""
test_presenters.py — Unit tests for Asana comment and JSON output builders.

No LLM, no MCP, no I/O. Uses pre-built TaskState objects.
"""
from __future__ import annotations

from typing import Any

import pytest

from marketing_agent_engine.domain.schemas import (
    AssigneeRecommendation,
    AssigneePlausibilityResult,
    BusinessUnitMatch,
    ClusterSlug,
    CompletenessFlag,
    CompletenessResult,
    PlausibilityVerdict,
    RoutingResult,
)
from marketing_agent_engine.domain.assignment_rules import AssignmentAnalysis
from marketing_agent_engine.flows.task_orchestrator_flow import ActionItem, TaskState
from marketing_agent_engine.presenters.asana_comment import build_asana_comment
from marketing_agent_engine.presenters.json_output import build_json_output


# ─────────────────────────────────────────────────────────────────────────────
# State factories
# ─────────────────────────────────────────────────────────────────────────────

def _routing(cluster: ClusterSlug = ClusterSlug.DACH_UND_HOLZ, confidence: float = 0.78) -> RoutingResult:
    return RoutingResult(
        business_unit=BusinessUnitMatch(
            slug="dach_flachdach",
            display_name="Dach – Flachdach",
            cluster=cluster,
            confidence=confidence,
            matched_by="keyword_scoring",
        ),
        cluster=cluster,
        cluster_coordinator_id="emp_004",
        confidence=confidence,
        resolution_path=["business_unit:dach_flachdach", "cluster:Dach_und_Holz"],
    )


def _completeness(score: float, missing: list[str] | None = None) -> CompletenessResult:
    m = missing or []
    all_criteria = [
        "title_present", "description_present", "due_date_set", "assignee_set",
        "project_assigned", "tags_present", "custom_fields_filled",
        "followers_present", "not_orphaned", "workspace_set", "permalink_present",
    ]
    flags = [
        CompletenessFlag(criterion=c, passed=(c not in m))
        for c in all_criteria
    ]
    return CompletenessResult(score=score, flags=flags, missing=m, warnings=[f"Missing: {x}" for x in m])


def _assignment(verdict: PlausibilityVerdict = PlausibilityVerdict.PLAUSIBLE) -> AssignmentAnalysis:
    av = AssigneePlausibilityResult(
        verdict=verdict,
        employee_id="emp_006",
        display_name="Felix Hoffmann",
        matched_skills=["social_media", "design"],
        missing_skills=[],
        explanation="Felix covers all required domains.",
    )
    rec = AssigneeRecommendation(
        employee_id="emp_006",
        display_name="Felix Hoffmann",
        confidence=0.85,
        matched_skills=["social_media", "design"],
        reason="Top recommendation.",
    )
    return AssignmentAnalysis(
        routing=_routing(),
        current_assignee_verdict=av,
        recommendations=[rec],
        needs_reassignment=(verdict != PlausibilityVerdict.PLAUSIBLE),
        reassignment_reason="" if verdict == PlausibilityVerdict.PLAUSIBLE else "Skill mismatch.",
        dry_run=True,
    )


def _state(
    next_step: str = "ready",
    score: float = 0.91,
    verdict: PlausibilityVerdict = PlausibilityVerdict.PLAUSIBLE,
    missing: list[str] | None = None,
    execution_mode: str = "dry_run",
) -> TaskState:
    state = TaskState(
        task_id="test-presenter-001",
        raw_input={"gid": "test-presenter-001"},
        next_step=next_step,
        execution_mode=execution_mode,
        timestamp="2025-04-15T10:00:00Z",
        routing=_routing(),
        assignment=_assignment(verdict),
        completeness=_completeness(score, missing),
        decision_trace={
            "routing": "Routed to Dach_und_Holz (confidence 0.78).",
            "assignment": f"Verdict: {verdict.value}.",
            "completeness": f"Score {score:.2f}.",
        },
        action_plan=[
            ActionItem(priority=1, action="Post analysis comment", owner="system", reason="Ticket ready."),
        ],
    )
    state.final_decision = {
        "next_step": next_step,
        "execution_mode": execution_mode,
        "timestamp": state.timestamp,
        "decision_trace": state.decision_trace,
    }
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Asana comment — structure
# ─────────────────────────────────────────────────────────────────────────────

class TestAsanaCommentStructure:
    def test_returns_non_empty_string(self) -> None:
        assert build_asana_comment(_state()) != ""

    def test_contains_workflow_state_label(self) -> None:
        comment = build_asana_comment(_state(next_step="ready"))
        assert "Bereit" in comment or "ready" in comment.lower()

    def test_contains_execution_mode(self) -> None:
        comment = build_asana_comment(_state(execution_mode="dry_run"))
        assert "dry_run" in comment.lower() or "DRY RUN" in comment

    def test_contains_cluster_name(self) -> None:
        comment = build_asana_comment(_state())
        assert "Dach" in comment

    def test_contains_coordinator_id(self) -> None:
        comment = build_asana_comment(_state())
        assert "emp_004" in comment

    def test_contains_assignee_verdict(self) -> None:
        comment = build_asana_comment(_state(verdict=PlausibilityVerdict.PLAUSIBLE))
        assert "Felix Hoffmann" in comment

    def test_contains_completeness_score(self) -> None:
        comment = build_asana_comment(_state(score=0.91))
        assert "91%" in comment or "0.91" in comment or "91" in comment

    def test_contains_next_step_description(self) -> None:
        comment = build_asana_comment(_state(next_step="blocked"))
        # Should have the German description for blocked
        assert "unvollständig" in comment or "Blockiert" in comment

    def test_missing_fields_listed_when_present(self) -> None:
        comment = build_asana_comment(_state(score=0.4, missing=["due_date_set", "assignee_set"]))
        assert "due_date_set" in comment
        assert "assignee_set" in comment

    def test_dry_run_footer_present(self) -> None:
        comment = build_asana_comment(_state(execution_mode="dry_run"))
        assert "DRY RUN" in comment

    def test_no_dry_run_footer_in_live_mode(self) -> None:
        comment = build_asana_comment(_state(execution_mode="live"))
        assert "DRY RUN" not in comment

    def test_decision_trace_present(self) -> None:
        comment = build_asana_comment(_state())
        assert "Entscheidungsbegründung" in comment or "Routing" in comment or "routing" in comment.lower()

    def test_action_plan_owner_present(self) -> None:
        comment = build_asana_comment(_state())
        assert "system" in comment.lower() or "System" in comment


# ─────────────────────────────────────────────────────────────────────────────
# JSON output — schema and fields
# ─────────────────────────────────────────────────────────────────────────────

class TestJsonOutputSchema:
    def test_returns_dict(self) -> None:
        assert isinstance(build_json_output(_state()), dict)

    def test_schema_version_is_1_0(self) -> None:
        assert build_json_output(_state())["schema_version"] == "1.0"

    def test_task_id_present(self) -> None:
        out = build_json_output(_state())
        assert out["task_id"] == "test-presenter-001"

    def test_execution_mode_present(self) -> None:
        out = build_json_output(_state(execution_mode="dry_run"))
        assert out["execution_mode"] == "dry_run"

    def test_simulated_true_in_dry_run(self) -> None:
        out = build_json_output(_state(execution_mode="dry_run"))
        assert out["simulated"] is True

    def test_simulated_false_in_live(self) -> None:
        out = build_json_output(_state(execution_mode="live"))
        assert out["simulated"] is False

    def test_confidence_summary_present(self) -> None:
        out = build_json_output(_state())
        cs = out["decision"]["confidence_summary"]
        assert "routing" in cs
        assert "assignment" in cs
        assert "completeness" in cs

    def test_routing_block_has_cluster(self) -> None:
        out = build_json_output(_state())
        assert out["routing"]["cluster"] == "Dach_und_Holz"

    def test_routing_confidence_correct(self) -> None:
        out = build_json_output(_state())
        assert out["routing"]["routing_confidence"] == pytest.approx(0.78)

    def test_assignment_verdict_present(self) -> None:
        out = build_json_output(_state(verdict=PlausibilityVerdict.PLAUSIBLE))
        assert out["assignment"]["verdict"] == "plausible"

    def test_completeness_score_present(self) -> None:
        out = build_json_output(_state(score=0.91))
        assert out["completeness"]["completeness_score"] == pytest.approx(0.91)

    def test_missing_has_severity(self) -> None:
        out = build_json_output(_state(score=0.4, missing=["due_date_set"]))
        missing = out["completeness"]["missing"]
        assert len(missing) == 1
        assert missing[0]["field"] == "due_date_set"
        assert missing[0]["severity"] == "high"

    def test_actions_list_non_empty(self) -> None:
        out = build_json_output(_state())
        assert isinstance(out["actions"], list)
        assert len(out["actions"]) >= 1

    def test_actions_have_id_field(self) -> None:
        out = build_json_output(_state())
        for action in out["actions"]:
            assert "id" in action
            assert action["id"].startswith("action_")

    def test_decision_trace_block_present(self) -> None:
        out = build_json_output(_state())
        dt = out["decision_trace"]
        assert "routing_reason" in dt
        assert "assignment_reason" in dt
        assert "completeness_reason" in dt

    def test_next_step_in_decision_block(self) -> None:
        out = build_json_output(_state(next_step="ready"))
        assert out["decision"]["next_step"] == "ready"

    def test_overall_status_present(self) -> None:
        out = build_json_output(_state(next_step="ready"))
        assert out["decision"]["overall_status"] == "ready"

    def test_blocked_status_is_blocked(self) -> None:
        out = build_json_output(_state(next_step="blocked", score=0.27))
        assert out["decision"]["overall_status"] == "blocked"
