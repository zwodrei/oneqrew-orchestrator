"""
CrewAI-compatible tools that wrap deterministic domain functions.

Each tool maps to exactly one domain function. Agents call these tools
rather than implementing any logic themselves.
"""

from __future__ import annotations

import json
from typing import Any

from crewai.tools import tool

from marketing_agent_engine.domain import (
    analyse_assignment,
    check_completeness,
    route_ticket,
)


@tool("route_ticket_tool")
def route_ticket_tool(ticket_json: str) -> str:
    """
    Route an Asana ticket to its cluster and business unit.

    Input: JSON string of an Asana ticket dict with keys:
      name, notes, projects (list with optional gid)

    Output: JSON string of RoutingResult with keys:
      cluster, business_unit, cluster_coordinator_id, confidence, resolution_path
    """
    try:
        ticket: dict[str, Any] = json.loads(ticket_json)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    title = ticket.get("name", "") or ""
    notes = ticket.get("notes", "") or ""
    projects = ticket.get("projects") or []
    asana_project_gid = (
        projects[0].get("gid") if projects and isinstance(projects[0], dict) else None
    )

    result = route_ticket(title, notes, asana_project_gid)
    return result.model_dump_json()


@tool("analyse_assignment_tool")
def analyse_assignment_tool(ticket_json: str, dry_run: bool = True) -> str:
    """
    Analyse the assignee plausibility and produce ranked recommendations.

    Input: JSON string of an Asana ticket dict.
    Output: JSON string of AssignmentAnalysis with keys:
      routing, current_assignee_verdict, recommendations,
      needs_reassignment, reassignment_reason, dry_run
    """
    try:
        ticket: dict[str, Any] = json.loads(ticket_json)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    result = analyse_assignment(ticket, dry_run=dry_run)
    return result.model_dump_json()


@tool("check_completeness_tool")
def check_completeness_tool(ticket_json: str) -> str:
    """
    Evaluate a ticket against the 11 completeness criteria.

    Input: JSON string of an Asana ticket dict.
    Output: JSON string of CompletenessResult with keys:
      score, passed, flags, missing, warnings
    """
    try:
        ticket: dict[str, Any] = json.loads(ticket_json)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    result = check_completeness(ticket)
    return result.model_dump_json()
