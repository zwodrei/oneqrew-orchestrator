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
    AssigneeRecommendation,
    AssigneePlausibilityResult,
    ClusterSlug,
    PlausibilityVerdict,
    RoutingResult,
)
from .skill_matching import evaluate_assignee_plausibility, recommend_assignees


class AssignmentAnalysis(BaseModel):
    routing: RoutingResult
    current_assignee_verdict: Optional[AssigneePlausibilityResult] = None
    recommendations: list[AssigneeRecommendation] = Field(default_factory=list)
    needs_reassignment: bool = False
    reassignment_reason: str = ""
    dry_run: bool = True


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

    current_assignee_data = ticket.get("assignee")
    current_verdict: Optional[AssigneePlausibilityResult] = None

    if current_assignee_data:
        emp = None
        if current_assignee_data.get("gid"):
            emp = get_employee_by_asana_gid(current_assignee_data["gid"])
        if emp is None and current_assignee_data.get("email"):
            from .employees import get_employee_by_email
            emp = get_employee_by_email(current_assignee_data["email"])

        if emp:
            current_verdict = evaluate_assignee_plausibility(emp.employee_id, title, notes)
        else:
            current_verdict = AssigneePlausibilityResult(
                verdict=PlausibilityVerdict.UNKNOWN,
                explanation=(
                    f"Assignee '{current_assignee_data.get('name', 'unknown')}'"
                    " not found in employee registry."
                ),
            )

    recommendations = recommend_assignees(title, notes, cluster_slug, top_n=3)

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

    return AssignmentAnalysis(
        routing=routing,
        current_assignee_verdict=current_verdict,
        recommendations=recommendations,
        needs_reassignment=needs_reassignment,
        reassignment_reason=reassignment_reason,
        dry_run=dry_run,
    )
