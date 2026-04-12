"""
Assignment rules: high-level API combining routing + skill matching for
the analysis crew agents. Provides plausibility checks and recommendations
with a unified, decision-ready interface.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from .employees import get_employee_by_asana_gid, get_employee_by_id
from .routing_rules import route_ticket
from .schemas import (
    AIReadiness,
    AssigneeRecommendation,
    AssigneePlausibilityResult,
    ClusterSlug,
    PlausibilityVerdict,
    RoutingResult,
    TaskCategory,
)
from .skill_matching import evaluate_assignee_plausibility, recommend_assignees
from .task_categorization import categorize_task, determine_ai_readiness_required


class AssignmentAnalysis(BaseModel):
    routing: RoutingResult
    current_assignee_verdict: Optional[AssigneePlausibilityResult] = None
    recommendations: list[AssigneeRecommendation] = Field(default_factory=list)
    needs_reassignment: bool = False
    reassignment_reason: str = ""
    dry_run: bool = True
    # New: task categorisation + AI-readiness routing
    task_category: Optional[str] = None
    ai_readiness_required: Optional[str] = None
    assignee_readiness: Optional[str] = None
    recommended_assignee_ai_level: Optional[str] = None
    assigned_by_skill_matrix: bool = False


def analyse_assignment(
    ticket: dict[str, Any],
    dry_run: bool = True,
) -> AssignmentAnalysis:
    """
    Full assignment analysis pipeline for a single Asana ticket dict.

    Steps:
      1. Route ticket → BU + cluster
      2. Evaluate current assignee plausibility (if any)
      3. Recommend top-3 alternative assignees
      4. Decide if reassignment is needed
    """
    title: str = ticket.get("name", "") or ""
    notes: str = ticket.get("notes", "") or ""
    asana_project_gid: Optional[str] = None
    projects = ticket.get("projects") or []
    if projects and isinstance(projects[0], dict):
        asana_project_gid = projects[0].get("gid")

    routing = route_ticket(title, notes, asana_project_gid)

    cluster_slug = routing.cluster.value if routing.cluster != ClusterSlug.UNBEKANNT else None

    # --- Task categorisation + AI-readiness requirement ---
    category: TaskCategory = categorize_task(title, notes)
    ai_readiness_required: AIReadiness = determine_ai_readiness_required(title, notes, category)

    current_assignee_data = ticket.get("assignee")
    current_verdict: Optional[AssigneePlausibilityResult] = None
    assignee_readiness_val: Optional[str] = None

    if current_assignee_data:
        emp = None
        if current_assignee_data.get("gid"):
            emp = get_employee_by_asana_gid(current_assignee_data["gid"])
        if emp is None and current_assignee_data.get("email"):
            from .employees import get_employee_by_email
            emp = get_employee_by_email(current_assignee_data["email"])

        if emp:
            current_verdict = evaluate_assignee_plausibility(
                emp.employee_id, title, notes, required_ai_readiness=ai_readiness_required
            )
            assignee_readiness_val = emp.ai_readiness.value
        else:
            current_verdict = AssigneePlausibilityResult(
                verdict=PlausibilityVerdict.UNKNOWN,
                explanation=(
                    f"Assignee '{current_assignee_data.get('name', 'unknown')}'"
                    " not found in employee registry."
                ),
            )

    recommendations = recommend_assignees(
        title, notes, cluster_slug, top_n=3,
        min_ai_readiness=ai_readiness_required,
    )
    assigned_by_skill_matrix = current_verdict is None  # True when no assignee → matrix picks

    # Derive recommended_assignee_ai_level from top recommendation
    recommended_ai_level: Optional[str] = None
    if recommendations:
        recommended_ai_level = recommendations[0].ai_readiness

    needs_reassignment = False
    reassignment_reason = ""

    if current_verdict is None:
        needs_reassignment = True
        reassignment_reason = "No assignee set."
    elif current_verdict.verdict == PlausibilityVerdict.IMPLAUSIBLE:
        needs_reassignment = True
        reassignment_reason = current_verdict.explanation
    elif current_verdict.verdict == PlausibilityVerdict.UNKNOWN:
        needs_reassignment = True
        reassignment_reason = "Current assignee unknown; verification required."
    elif current_verdict.human_review_required:
        needs_reassignment = True
        reassignment_reason = (
            f"AI-Readiness mismatch: assignee is {assignee_readiness_val}, "
            f"task requires {ai_readiness_required.value}."
        )

    return AssignmentAnalysis(
        routing=routing,
        current_assignee_verdict=current_verdict,
        recommendations=recommendations,
        needs_reassignment=needs_reassignment,
        reassignment_reason=reassignment_reason,
        dry_run=dry_run,
        task_category=category.value,
        ai_readiness_required=ai_readiness_required.value,
        assignee_readiness=assignee_readiness_val,
        recommended_assignee_ai_level=recommended_ai_level,
        assigned_by_skill_matrix=assigned_by_skill_matrix,
    )
