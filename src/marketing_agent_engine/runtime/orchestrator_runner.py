"""
OrchestratorRunner — the end-to-end pipeline entry point.

Pipeline:
  raw ticket input
    → TaskOrchestratorFlow  (control + analysis)
    → build_asana_comment() (human-readable output)
    → build_json_output()   (machine-readable output)
    → execute_actions()     (MCP write — guarded by DRY_RUN)

Hard rules:
  - Flow is the SINGLE source of control
  - Presenters ONLY format, never decide
  - MCP is called ONLY here, ONLY after flow completes
  - DRY_RUN=true → all MCP writes return simulated responses
  - Phase 1: only create_comment allowed (no update_task)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from marketing_agent_engine.config.settings import settings
from marketing_agent_engine.mcp.guarded_client import GuardedMCPClient, make_guarded_client
from marketing_agent_engine.mcp.tools import ToolResponse
from marketing_agent_engine.presenters.asana_comment import build_asana_comment
from marketing_agent_engine.presenters.json_output import build_json_output

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Output container
# ---------------------------------------------------------------------------

@dataclass
class RunResult:
    task_id: str
    next_step: str
    execution_mode: str
    comment: str
    json_output: dict[str, Any]
    mcp_responses: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def simulated(self) -> bool:
        return self.execution_mode == "dry_run"

    def summary(self) -> str:
        status = "DRY RUN" if self.simulated else "LIVE"
        mcp_count = len(self.mcp_responses)
        err_count = len(self.errors)
        return (
            f"[{status}] task_id={self.task_id} | "
            f"next_step={self.next_step} | "
            f"mcp_calls={mcp_count} | "
            f"errors={err_count}"
        )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

class OrchestratorRunner:
    """
    Wires the full pipeline: Flow → Presenters → MCP.

    Usage:
        runner = OrchestratorRunner()
        result = runner.run(ticket_dict)
        print(result.comment)
        print(result.json_output)
    """

    def __init__(self, mcp_client: Optional[GuardedMCPClient] = None) -> None:
        self._mcp = mcp_client or make_guarded_client()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self, ticket: dict[str, Any]) -> RunResult:
        """
        Execute the full pipeline for one Asana ticket dict.

        Args:
            ticket: Raw Asana task dict (gid, name, notes, assignee, …)

        Returns:
            RunResult with comment, json_output, and mcp_responses.
        """
        task_id = ticket.get("gid") or ticket.get("id") or ticket.get("name", "unknown")[:60]
        logger.info("OrchestratorRunner.run: task_id=%s mode=%s", task_id, settings.dry_run)
        _start = time.monotonic()

        # 1. Run the flow
        from marketing_agent_engine.flows.task_orchestrator_flow import TaskOrchestratorFlow

        flow = TaskOrchestratorFlow()
        flow.state.raw_input = ticket
        flow.kickoff()
        state = flow.state

        _log_state(state)

        # 2. Build outputs
        comment = build_asana_comment(state)
        json_out = build_json_output(state)

        # 3. Execute or simulate MCP actions
        mcp_responses: list[dict[str, Any]] = []
        errors: list[str] = []

        try:
            mcp_responses = self._execute_actions(state, comment)
        except Exception as exc:
            logger.error("execute_actions failed: %s", exc, exc_info=True)
            errors.append(str(exc))

        duration_ms = int((time.monotonic() - _start) * 1000)
        _log_structured(state, duration_ms, errors)

        result = RunResult(
            task_id=str(state.task_id),
            next_step=state.next_step,
            execution_mode=state.execution_mode,
            comment=comment,
            json_output=json_out,
            mcp_responses=mcp_responses,
            errors=errors,
        )

        logger.info(result.summary())
        return result

    # ------------------------------------------------------------------
    # MCP execution (Phase 1: create_comment only)
    # ------------------------------------------------------------------

    def _execute_actions(
        self,
        state: Any,
        comment: str,
    ) -> list[dict[str, Any]]:
        """
        Post the analysis comment to Asana via GuardedMCPClient.

        In DRY_RUN mode the GuardedMCPClient intercepts the call and
        returns a simulated response — Asana is never contacted.

        Phase 1 restriction: only create_comment is called.
        update_task is intentionally omitted.
        """
        task_id = state.task_id
        next_step = state.next_step
        responses: list[dict[str, Any]] = []

        if not next_step:
            logger.warning("next_step is empty — skipping MCP execution.")
            return responses

        # All next_step values result in a comment (different tone per step)
        comment_text = _comment_for_step(next_step, comment)

        logger.info(
            "Calling create_comment: task_id=%s next_step=%s dry_run=%s",
            task_id, next_step, settings.dry_run,
        )

        with self._mcp as client:
            resp: ToolResponse = client.create_comment(
                task_id=str(task_id),
                text=comment_text,
                is_pinned=(next_step in ("blocked", "needs_assignment")),
            )

        responses.append({
            "tool": "create_comment",
            "task_id": str(task_id),
            "next_step": next_step,
            "simulated": resp.simulated,
            "execution_mode": resp.execution_mode,
            "success": resp.success,
            "data": resp.data,
            "error": resp.error,
        })

        return responses


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _comment_for_step(next_step: str, full_comment: str) -> str:
    """
    Returns the full formatted comment — the step context is already
    embedded by build_asana_comment(). This hook exists so future
    phases can add step-specific preambles without changing the presenter.
    """
    return full_comment


def _log_state(state: Any) -> None:
    action_count = len(state.action_plan) if state.action_plan else 0
    logger.info(
        "Flow complete: task_id=%s | next_step=%s | execution_mode=%s | actions=%d",
        state.task_id,
        state.next_step,
        state.execution_mode,
        action_count,
    )
    if state.analysis_error:
        logger.error("Analysis error: %s", state.analysis_error)


def _log_structured(state: Any, duration_ms: int, errors: list[str]) -> None:
    """
    Emit one structured JSON log line per run (Phase C).

    Fields logged:
      task_id, next_step, execution_mode, timestamp, duration_ms, error
    Never logs API keys or sensitive task content.
    """
    entry = {
        "task_id": str(state.task_id),
        "next_step": state.next_step,
        "execution_mode": state.execution_mode,
        "timestamp": state.timestamp,
        "duration_ms": duration_ms,
        "error": errors[0] if errors else None,
    }
    logger.info("RUN_SUMMARY %s", json.dumps(entry))
