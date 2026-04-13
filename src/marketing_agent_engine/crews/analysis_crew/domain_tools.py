"""
CrewAI-compatible tools that wrap deterministic domain functions.

Each tool maps to exactly one domain function. Agents call these tools
rather than implementing any logic themselves.
"""

from __future__ import annotations

import json
from typing import Any

from crewai.tools import BaseTool

from marketing_agent_engine.domain import (
    analyse_assignment,
    check_completeness,
    route_ticket,
)
from pydantic import BaseModel, Field

class EmptyInput(BaseModel):
    """Empty input schema."""
    pass

class RouteTicketTool(BaseTool):
    name: str = "route_ticket_tool"
    description: str = (
        "Route an Asana ticket to its cluster and business unit. "
        "Outputs JSON string of RoutingResult. "
        "No input arguments required."
    )
    args_schema: type[BaseModel] = EmptyInput
    ticket: dict[str, Any]

    def _run(self) -> str:
        ticket = self.ticket
        title = ticket.get("name", "") or ""
        notes = ticket.get("notes", "") or ""
        projects = ticket.get("projects") or []
        asana_project_gid = (
            projects[0].get("gid") if projects and isinstance(projects[0], dict) else None
        )

        result = route_ticket(title, notes, asana_project_gid)
        return result.model_dump_json()

class AnalyseAssignmentTool(BaseTool):
    name: str = "analyse_assignment_tool"
    description: str = (
        "Analyse the assignee plausibility and produce ranked recommendations. "
        "Outputs JSON string of AssignmentAnalysis. "
        "No input arguments required."
    )
    args_schema: type[BaseModel] = EmptyInput
    ticket: dict[str, Any]
    dry_run: bool = True

    def _run(self) -> str:
        result = analyse_assignment(self.ticket, dry_run=self.dry_run)
        return result.model_dump_json()

class CheckCompletenessTool(BaseTool):
    name: str = "check_completeness_tool"
    description: str = (
        "Evaluate a ticket against the completeness criteria. "
        "Outputs JSON string of CompletenessResult. "
        "No input arguments required."
    )
    args_schema: type[BaseModel] = EmptyInput
    ticket: dict[str, Any]

    def _run(self) -> str:
        result = check_completeness(self.ticket)
        return result.model_dump_json()
