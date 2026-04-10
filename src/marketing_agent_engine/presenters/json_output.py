"""
JSON output builder.

Transforms a completed TaskState into a clean, machine-readable dict
suitable for logging, downstream systems, or API responses.

Rules:
  - NO business logic
  - NO decisions
  - ONLY structured transformation from state data
  - Preserves ALL important nested fields
  - Adds simulated=true flag when execution_mode == "dry_run"
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from marketing_agent_engine.flows.task_orchestrator_flow import TaskState

SCHEMA_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Severity mapping for missing completeness fields
# ---------------------------------------------------------------------------

# Fields with no assignee, no title, no project = high; tags/custom = medium; system = low
_MISSING_FIELD_SEVERITY: dict[str, str] = {
    "title_present": "high",
    "description_present": "high",
    "due_date_set": "high",
    "assignee_set": "high",
    "project_assigned": "high",
    "tags_present": "medium",
    "custom_fields_filled": "medium",
    "followers_present": "medium",
    "not_orphaned": "medium",
    "workspace_set": "low",
    "permalink_present": "low",
}

# ---------------------------------------------------------------------------
# Action type mapping
# ---------------------------------------------------------------------------

_NEXT_STEP_ACTION_TYPES: dict[str, str] = {
    "blocked": "request_core_information",
    "needs_information": "request_missing_details",
    "needs_assignment": "assign_recommended_person",
    "review": "escalate_to_coordinator",
    "ready": "post_comment_and_proceed",
    "": "manual_review",
}

_NEXT_STEP_OVERALL_STATUS: dict[str, str] = {
    "blocked": "blocked",
    "needs_information": "needs_attention",
    "needs_assignment": "needs_attention",
    "review": "needs_attention",
    "ready": "ready",
    "": "unknown",
}


# ---------------------------------------------------------------------------
# Public builder
# ---------------------------------------------------------------------------

def build_json_output(state: "TaskState") -> dict[str, Any]:
    """
    Build a clean, machine-readable JSON dict from a completed TaskState.
    """
    routing = state.routing
    assignment = state.assignment
    completeness = state.completeness

    # --- Routing block ---
    routing_block: dict[str, Any] = {
        "cluster": routing.cluster.value if routing else "unbekannt",
        "business_unit_slug": (
            routing.business_unit.slug if routing and routing.business_unit else None
        ),
        "business_unit_display_name": (
            routing.business_unit.display_name if routing and routing.business_unit else None
        ),
        "routing_confidence": routing.confidence if routing else 0.0,
        "coordinator_id": routing.cluster_coordinator_id if routing else None,
        "resolution_path": routing.resolution_path if routing else [],
    }

    # --- Assignment block ---
    av = assignment.current_assignee_verdict if assignment else None
    top_rec = assignment.recommendations[0] if assignment and assignment.recommendations else None

    assignment_block: dict[str, Any] = {
        "verdict": av.verdict.value if av else "unknown",
        "employee_id": av.employee_id if av else None,
        "display_name": av.display_name if av else None,
        "matched_skills": av.matched_skills if av else [],
        "missing_skills": av.missing_skills if av else [],
        "assignment_confidence": _assignment_confidence(av),
        "needs_reassignment": assignment.needs_reassignment if assignment else True,
        "reassignment_reason": assignment.reassignment_reason if assignment else "",
        "top_recommendation": {
            "employee_id": top_rec.employee_id,
            "display_name": top_rec.display_name,
            "confidence": top_rec.confidence,
            "matched_skills": top_rec.matched_skills,
            "reason": top_rec.reason,
        } if top_rec else None,
        "all_recommendations": [
            {
                "employee_id": r.employee_id,
                "display_name": r.display_name,
                "confidence": r.confidence,
                "matched_skills": r.matched_skills,
            }
            for r in (assignment.recommendations if assignment else [])
        ],
    }

    # --- Completeness block ---
    flags_summary = []
    missing_with_severity: list[dict[str, str]] = []
    if completeness:
        flags_summary = [
            {"criterion": f.criterion, "passed": f.passed, "note": f.note}
            for f in completeness.flags
            if not f.passed
        ]
        missing_with_severity = [
            {
                "field": m,
                "severity": _MISSING_FIELD_SEVERITY.get(m, "medium"),
            }
            for m in completeness.missing
        ]

    completeness_block: dict[str, Any] = {
        "completeness_score": completeness.score if completeness else 0.0,
        "passed": completeness.passed if completeness else False,
        "missing": missing_with_severity,
        "warnings": completeness.warnings if completeness else [],
        "failed_flags": flags_summary,
    }

    # --- Decision block ---
    next_step = state.next_step or ""
    action_type = _NEXT_STEP_ACTION_TYPES.get(next_step, "manual_review")
    overall_status = _NEXT_STEP_OVERALL_STATUS.get(next_step, "unknown")

    decision_block: dict[str, Any] = {
        "next_step": next_step,
        "overall_status": overall_status,
        "confidence_summary": {
            "routing": routing.confidence if routing else 0.0,
            "assignment": _assignment_confidence(av),
            "completeness": completeness.score if completeness else 0.0,
        },
    }

    # --- Actions block ---
    actions: list[dict[str, Any]] = []
    if state.action_plan:
        for idx, item in enumerate(state.action_plan, start=1):
            actions.append({
                "id": f"action_{idx}",
                "type": action_type,
                "description": item.action,
                "priority": item.priority,
                "owner": item.owner,
                "reason": item.reason,
            })
    else:
        actions.append({
            "id": "action_1",
            "type": action_type,
            "description": _default_action_description(next_step),
            "priority": 1,
            "owner": "coordinator",
            "reason": "Auto-generated from next_step.",
        })

    # --- Decision trace block ---
    trace = state.decision_trace or {}
    decision_trace_block: dict[str, str] = {
        "routing_reason": trace.get("routing", ""),
        "assignment_reason": trace.get("assignment", ""),
        "completeness_reason": trace.get("completeness", ""),
    }

    # --- Assemble ---
    output: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "task_id": state.task_id,
        "execution_mode": state.execution_mode,
        "timestamp": state.timestamp,
        "simulated": state.execution_mode == "dry_run",
        "routing": routing_block,
        "assignment": assignment_block,
        "completeness": completeness_block,
        "decision": decision_block,
        "actions": actions,
        "decision_trace": decision_trace_block,
    }

    # Merge any extra fields from the synthesizer's final_decision
    # (model_used, overall_status already covered, avoid overwriting structured blocks)
    _SKIP_KEYS = frozenset({"routing", "assignment", "completeness", "decision", "actions"})
    for k, v in state.final_decision.items():
        if k not in output and k not in _SKIP_KEYS:
            output[k] = v

    return output


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assignment_confidence(av: Any) -> float:
    from marketing_agent_engine.domain.schemas import PlausibilityVerdict
    if av is None:
        return 0.0
    verdict_scores = {
        PlausibilityVerdict.PLAUSIBLE: 1.0,
        PlausibilityVerdict.QUESTIONABLE: 0.5,
        PlausibilityVerdict.IMPLAUSIBLE: 0.1,
        PlausibilityVerdict.UNKNOWN: 0.0,
    }
    return verdict_scores.get(av.verdict, 0.0)


def _default_action_description(next_step: str) -> str:
    return {
        "blocked": "Request missing core information from ticket creator.",
        "needs_information": "Request missing details from ticket requester.",
        "needs_assignment": "Assign recommended person to ticket.",
        "review": "Escalate assignment to cluster coordinator for review.",
        "ready": "Post analysis comment and proceed with ticket execution.",
    }.get(next_step, "Manual review required.")
