"""
TaskOrchestratorFlow — the control layer for the Marketing Agent Engine.

Responsibilities:
  - Receive raw Asana ticket input
  - Delegate analysis to AnalysisCrew (no business logic here)
  - Interpret deterministic domain results to decide next_step
  - Route to the appropriate handler
  - Prepare action plan (NO MCP writes here)

MCP write calls happen OUTSIDE this flow, after it returns.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel, Field

from marketing_agent_engine.config.settings import settings
from marketing_agent_engine.domain.assignment_rules import AssignmentAnalysis
from marketing_agent_engine.domain.schemas import (
    AssigneePlausibilityResult,
    ClusterSlug,
    CompletenessResult,
    PlausibilityVerdict,
    RoutingResult,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPLETENESS_BLOCK_THRESHOLD = 0.5   # below this → blocked
COMPLETENESS_WARN_THRESHOLD = 0.7    # below this → needs_information
ROUTING_CONFIDENCE_WARN = 0.4        # below this → route flagged as uncertain


# ---------------------------------------------------------------------------
# State model
# ---------------------------------------------------------------------------

class ActionItem(BaseModel):
    priority: int
    action: str
    owner: str
    reason: str


class TaskState(BaseModel):
    # Input
    task_id: str = ""
    raw_input: dict[str, Any] = Field(default_factory=dict)

    # Analysis results (populated after run_analysis)
    routing: Optional[RoutingResult] = None
    assignment: Optional[AssignmentAnalysis] = None
    completeness: Optional[CompletenessResult] = None
    final_decision: dict[str, Any] = Field(default_factory=dict)

    # Decision outputs (populated after make_decision)
    next_step: str = ""
    action_plan: list[ActionItem] = Field(default_factory=list)
    execution_mode: str = "dry_run"
    timestamp: str = ""

    # Diagnostics
    analysis_error: Optional[str] = None
    decision_trace: dict[str, str] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Flow
# ---------------------------------------------------------------------------

class TaskOrchestratorFlow(Flow[TaskState]):
    """
    Sequential orchestration flow for a single Asana marketing ticket.

    Step order:
      start_flow → run_analysis → make_decision → router → handler

    Test hook:
      Set `_analysis_override` to a callable(ticket) -> dict before kickoff
      to bypass AnalysisCrew (no LLM needed in tests/scripts).
    """

    _analysis_override: Any = None  # callable(ticket) -> dict, for testing

    # ------------------------------------------------------------------
    # Step 1: Initialise state from raw input
    # ------------------------------------------------------------------

    @start()
    def start_flow(self) -> None:
        raw = self.state.raw_input
        self.state.task_id = (
            raw.get("gid")
            or raw.get("id")
            or raw.get("name", "unknown")[:60]
        )
        self.state.execution_mode = "dry_run" if settings.dry_run else "live"
        self.state.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        logger.info("Flow started: task_id=%s mode=%s", self.state.task_id, self.state.execution_mode)

    # ------------------------------------------------------------------
    # Step 2: Run the 4-agent AnalysisCrew
    # ------------------------------------------------------------------

    @listen("start_flow")
    def run_analysis(self) -> None:
        logger.info("Running AnalysisCrew for task_id=%s", self.state.task_id)
        try:
            if self._analysis_override is not None:
                decision = self._analysis_override(self.state.raw_input)
            else:
                from marketing_agent_engine.crews.analysis_crew.crew import AnalysisCrew
                decision = AnalysisCrew(ticket=self.state.raw_input).analyse()

            self.state.final_decision = decision
            self.state.routing = _parse_routing(decision)
            self.state.assignment = _parse_assignment(decision)
            self.state.completeness = _parse_completeness(decision)

        except Exception as exc:
            logger.error("AnalysisCrew failed: %s", exc, exc_info=True)
            self.state.analysis_error = str(exc)
            # Safe defaults so decision step can still produce a result
            self.state.routing = None
            self.state.assignment = None
            self.state.completeness = None

    # ------------------------------------------------------------------
    # Step 3: Deterministic decision logic
    # ------------------------------------------------------------------

    @listen("run_analysis")
    def make_decision(self) -> None:
        if self.state.analysis_error:
            self.state.next_step = "blocked"
            self.state.decision_trace = {
                "routing": "Analysis failed — no routing result available.",
                "assignment": "Analysis failed — no assignment result available.",
                "completeness": f"Analysis error: {self.state.analysis_error}",
            }
            return

        completeness = self.state.completeness
        assignment = self.state.assignment
        routing = self.state.routing

        # --- Routing trace ---
        if routing:
            cluster = routing.cluster.value if routing.cluster else "unbekannt"
            bu = routing.business_unit.slug if routing.business_unit else "none"
            conf = routing.confidence
            routing_trace = (
                f"Routed to cluster '{cluster}' (BU: {bu}) "
                f"via {routing.resolution_path[0] if routing.resolution_path else 'unknown'} "
                f"with confidence {conf:.2f}."
            )
        else:
            cluster = "unbekannt"
            conf = 0.0
            routing_trace = "Routing not available."

        # --- Completeness trace + threshold check ---
        if completeness:
            score = completeness.score
            passed_count = sum(1 for f in completeness.flags if f.passed)
            total = len(completeness.flags)
            failed = completeness.missing
            completeness_trace = (
                f"Score {score:.2f} ({passed_count}/{total} criteria passed)"
                + (f"; failed: {', '.join(failed)}." if failed else ".")
            )
        else:
            score = 0.0
            completeness_trace = "Completeness not available."

        # --- Assignment trace + verdict ---
        verdict = PlausibilityVerdict.UNKNOWN
        assignee_present = False
        if assignment:
            av = assignment.current_assignee_verdict
            if av:
                verdict = av.verdict
                assignee_present = bool(av.employee_id)
                matched = ", ".join(av.matched_skills) or "none"
                missing_skills = ", ".join(av.missing_skills) or "none"
                assignment_trace = (
                    f"Assignee verdict: {verdict.value}; "
                    f"matched skills: {matched}; missing: {missing_skills}."
                )
            else:
                assignment_trace = "No assignee set on ticket."
        else:
            assignment_trace = "Assignment analysis not available."

        # --- Decision ---
        if score < COMPLETENESS_BLOCK_THRESHOLD:
            next_step = "blocked"
        elif score < COMPLETENESS_WARN_THRESHOLD:
            next_step = "needs_information"
        elif not assignee_present:
            next_step = "needs_assignment"
        elif verdict in (PlausibilityVerdict.IMPLAUSIBLE, PlausibilityVerdict.QUESTIONABLE):
            next_step = "review"
        else:
            next_step = "ready"

        self.state.next_step = next_step
        self.state.decision_trace = {
            "routing": routing_trace,
            "assignment": assignment_trace,
            "completeness": completeness_trace,
        }
        logger.info("Decision: next_step=%s (score=%.2f, verdict=%s)", next_step, score, verdict.value)

    # ------------------------------------------------------------------
    # Step 4: Router → dispatch to handler
    # ------------------------------------------------------------------

    @router("make_decision")
    def route_next(self) -> str:
        return self.state.next_step

    # ------------------------------------------------------------------
    # Handlers — prepare action plan ONLY, no MCP calls
    # ------------------------------------------------------------------

    @listen("blocked")
    def handle_blocked(self) -> None:
        completeness = self.state.completeness
        missing = completeness.missing if completeness else ["unknown"]
        self.state.action_plan = [
            ActionItem(
                priority=1,
                action="Return ticket to requester for completion",
                owner="requester",
                reason=f"Completeness score below {COMPLETENESS_BLOCK_THRESHOLD:.0%}. "
                       f"Missing: {', '.join(missing[:5])}.",
            ),
            ActionItem(
                priority=2,
                action="Add ticket to 'incomplete' backlog",
                owner="coordinator",
                reason="Blocked tickets must not enter the analysis queue.",
            ),
        ]
        self._finalize()

    @listen("needs_information")
    def handle_missing_info(self) -> None:
        completeness = self.state.completeness
        missing = completeness.missing if completeness else []
        self.state.action_plan = [
            ActionItem(
                priority=1,
                action="Request missing fields from ticket requester",
                owner="requester",
                reason=f"Missing: {', '.join(missing)}.",
            ),
            ActionItem(
                priority=2,
                action="Flag ticket for follow-up in 48h",
                owner="coordinator",
                reason="Incomplete tickets must be resolved before assignment.",
            ),
        ]
        self._finalize()

    @listen("needs_assignment")
    def handle_assignment(self) -> None:
        assignment = self.state.assignment
        routing = self.state.routing
        top_rec = None
        if assignment and assignment.recommendations:
            top_rec = assignment.recommendations[0]

        plan = [
            ActionItem(
                priority=1,
                action=(
                    f"Assign ticket to {top_rec.display_name}"
                    if top_rec else "Assign ticket manually"
                ),
                owner=(
                    routing.cluster_coordinator_id
                    if routing and routing.cluster_coordinator_id else "coordinator"
                ),
                reason=(
                    f"No assignee set. Top recommendation: {top_rec.display_name} "
                    f"(confidence {top_rec.confidence:.0%}, skills: {', '.join(top_rec.matched_skills)})."
                    if top_rec else "No assignee set and no recommendation available."
                ),
            ),
        ]
        if routing and routing.cluster != ClusterSlug.UNBEKANNT:
            plan.append(ActionItem(
                priority=2,
                action="Notify cluster coordinator of unassigned ticket",
                owner=routing.cluster_coordinator_id or "coordinator",
                reason=f"Cluster {routing.cluster.value} coordinator must validate assignment.",
            ))
        self.state.action_plan = plan
        self._finalize()

    @listen("review")
    def handle_review(self) -> None:
        assignment = self.state.assignment
        routing = self.state.routing
        av = assignment.current_assignee_verdict if assignment else None

        self.state.action_plan = [
            ActionItem(
                priority=1,
                action="Flag current assignment for coordinator review",
                owner=(
                    routing.cluster_coordinator_id
                    if routing and routing.cluster_coordinator_id else "coordinator"
                ),
                reason=av.explanation if av else "Assignment plausibility is questionable.",
            ),
            ActionItem(
                priority=2,
                action=(
                    f"Consider reassigning to {assignment.recommendations[0].display_name}"
                    if assignment and assignment.recommendations else "Review assignee skills manually"
                ),
                owner="coordinator",
                reason=(
                    f"Top recommendation has confidence "
                    f"{assignment.recommendations[0].confidence:.0%}."
                    if assignment and assignment.recommendations else "No recommendation available."
                ),
            ),
        ]
        self._finalize()

    @listen("ready")
    def handle_ready(self) -> None:
        assignment = self.state.assignment
        routing = self.state.routing
        av = assignment.current_assignee_verdict if assignment else None

        self.state.action_plan = [
            ActionItem(
                priority=1,
                action="Post analysis summary as Asana comment",
                owner="system",
                reason=(
                    f"Assignment is {av.verdict.value if av else 'verified'}. "
                    f"Routing confidence: {routing.confidence:.0%}."
                    if routing else "Ticket is ready for execution."
                ),
            ),
        ]
        self._finalize()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _finalize(self) -> None:
        """Merge decision_trace and action_plan into final_decision.

        Phase E: sets requires_human=True when next_step is 'review'
        so downstream systems can flag the ticket without implementing UI.
        """
        self.state.final_decision.update({
            "next_step": self.state.next_step,
            "execution_mode": self.state.execution_mode,
            "timestamp": self.state.timestamp,
            "decision_trace": self.state.decision_trace,
            "action_plan": [a.model_dump() for a in self.state.action_plan],
            "requires_human": self.state.next_step == "review",
        })

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, ticket: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the full orchestration flow for one Asana ticket.

        Returns the final_decision dict with next_step, action_plan,
        execution_mode, and decision_trace.
        """
        self.state.raw_input = ticket
        self.kickoff()
        return {
            "next_step": self.state.next_step,
            "execution_mode": self.state.execution_mode,
            "decision": self.state.final_decision,
        }


# ---------------------------------------------------------------------------
# Helpers: parse domain objects from synthesizer JSON
# ---------------------------------------------------------------------------

def _parse_routing(decision: dict[str, Any]) -> Optional[RoutingResult]:
    """Reconstruct a minimal RoutingResult from the synthesizer output dict."""
    try:
        r = decision.get("routing", {})
        from marketing_agent_engine.domain.schemas import BusinessUnitMatch
        bu_slug = r.get("business_unit_slug") or r.get("business_unit", {}).get("slug") if isinstance(r.get("business_unit"), dict) else r.get("business_unit_slug")
        bu = None
        if bu_slug:
            from marketing_agent_engine.domain.business_units import get_business_unit_by_slug
            src_bu = get_business_unit_by_slug(bu_slug)
            if src_bu:
                bu = BusinessUnitMatch(
                    slug=src_bu.slug,
                    display_name=src_bu.display_name,
                    cluster=src_bu.cluster,
                    confidence=r.get("routing_confidence", 0.0),
                    matched_by="synthesis",
                )
        cluster_val = r.get("cluster", "unbekannt")
        try:
            cluster = ClusterSlug(cluster_val)
        except ValueError:
            cluster = ClusterSlug.UNBEKANNT
        return RoutingResult(
            business_unit=bu,
            cluster=cluster,
            cluster_coordinator_id=r.get("coordinator_id"),
            confidence=r.get("routing_confidence", 0.0),
            resolution_path=[f"synthesis:{cluster_val}"],
        )
    except Exception as exc:
        logger.warning("Could not parse routing from decision: %s", exc)
        return None


def _parse_assignment(decision: dict[str, Any]) -> Optional[AssignmentAnalysis]:
    """Reconstruct a minimal AssignmentAnalysis from the synthesizer output dict."""
    try:
        a = decision.get("assignment", {})
        verdict_str = a.get("verdict", "unknown")
        try:
            verdict = PlausibilityVerdict(verdict_str)
        except ValueError:
            verdict = PlausibilityVerdict.UNKNOWN

        # Preserve employee_id / display_name so make_decision can detect
        # whether an assignee is present (employee_id present → assignee set).
        current_employee_id: Optional[str] = a.get("employee_id") or a.get("assignee_id")
        current_display_name: Optional[str] = a.get("display_name") or a.get("assignee_name")

        # If verdict is plausible/questionable/implausible but no explicit
        # employee_id was supplied, synthesise a placeholder so the flow can
        # distinguish "assignee unknown identity" from "no assignee at all".
        if verdict in (
            PlausibilityVerdict.PLAUSIBLE,
            PlausibilityVerdict.QUESTIONABLE,
            PlausibilityVerdict.IMPLAUSIBLE,
        ) and not current_employee_id:
            current_employee_id = "assignee_from_synthesis"

        av = AssigneePlausibilityResult(
            verdict=verdict,
            employee_id=current_employee_id,
            display_name=current_display_name,
            explanation=a.get("reassignment_reason", ""),
        )
        top = a.get("top_recommendation") or {}
        from marketing_agent_engine.domain.schemas import AssigneeRecommendation
        recs = []
        if top and top.get("employee_id"):
            recs = [AssigneeRecommendation(
                employee_id=top["employee_id"],
                display_name=top.get("display_name", ""),
                confidence=top.get("confidence", 0.0),
                matched_skills=top.get("matched_skills", []),
                reason=a.get("reassignment_reason", ""),
            )]
        return AssignmentAnalysis(
            routing=_parse_routing(decision) or RoutingResult(
                cluster=ClusterSlug.UNBEKANNT, confidence=0.0
            ),
            current_assignee_verdict=av,
            recommendations=recs,
            needs_reassignment=a.get("needs_reassignment", False),
            reassignment_reason=a.get("reassignment_reason", ""),
            dry_run=settings.dry_run,
        )
    except Exception as exc:
        logger.warning("Could not parse assignment from decision: %s", exc)
        return None


def _parse_completeness(decision: dict[str, Any]) -> Optional[CompletenessResult]:
    """Reconstruct a minimal CompletenessResult from the synthesizer output dict."""
    try:
        from marketing_agent_engine.domain.schemas import CompletenessFlag
        c = decision.get("completeness", {})
        score = float(c.get("completeness_score", c.get("score", 0.0)))
        missing = c.get("critical_missing") or c.get("missing", [])
        flags = [CompletenessFlag(criterion=m, passed=False) for m in missing]
        return CompletenessResult(
            score=score,
            flags=flags,
            missing=missing,
            warnings=[f"Missing: {m}" for m in missing],
        )
    except Exception as exc:
        logger.warning("Could not parse completeness from decision: %s", exc)
        return None
