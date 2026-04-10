"""
GuardedMCPClient — safety wrapper enforcing DRY_RUN semantics.

Rules:
  - READ tools  (get_task_by_id, get_comments) → always allowed
  - WRITE tools (create_comment, update_task)  → blocked when DRY_RUN=true
    → returns a SimulatedWriteResponse instead of calling Asana
  - If DRY_RUN=false and a write is attempted, the real MCP client is called

The guard layer is the ONLY place where dry-run decisions are made.
No other module should call MCPClient.call_tool() directly.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from .client import MCPClient
from .tools import (
    ALL_TOOLS,
    READ_TOOLS,
    WRITE_TOOLS,
    CreateCommentRequest,
    GetCommentsRequest,
    GetTaskByIdRequest,
    SimulatedWriteResponse,
    ToolResponse,
    UpdateTaskRequest,
)

logger = logging.getLogger(__name__)


class DryRunViolationError(RuntimeError):
    """Raised when a write tool is called with an unexpected non-dry-run config."""


class GuardedMCPClient:
    """
    Safe facade over MCPClient with enforced dry-run control.

    Usage:
        client = GuardedMCPClient(dry_run=True)
        with client:
            task  = client.get_task_by_id("123456789")
            reply = client.create_comment("123456789", "Analysis complete.")
            # In dry-run: reply.data["simulated"] == True
    """

    def __init__(
        self,
        dry_run: bool = True,
        mcp_client: Optional[MCPClient] = None,
    ) -> None:
        self.dry_run = dry_run
        self._client = mcp_client or MCPClient()

        if not dry_run:
            logger.warning(
                "GuardedMCPClient: DRY_RUN=false — WRITE operations will reach Asana."
            )
        else:
            logger.info("GuardedMCPClient: DRY_RUN=true — all writes are simulated.")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self._client.connect()

    def disconnect(self) -> None:
        self._client.disconnect()

    def __enter__(self) -> "GuardedMCPClient":
        self.connect()
        return self

    def __exit__(self, *_: Any) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # Guard logic
    # ------------------------------------------------------------------

    def _guard_write(self, tool_name: str, payload: dict[str, Any]) -> Optional[ToolResponse]:
        """
        If dry_run is active, return a simulated response without calling Asana.
        Returns None if the call should proceed to the real client.
        """
        if not self.dry_run:
            return None

        logger.info(
            "DRY_RUN: blocking write tool '%s' with payload %s",
            tool_name,
            payload,
        )
        simulated = SimulatedWriteResponse(action=tool_name, payload=payload)
        resp = simulated.as_tool_response()
        resp.execution_mode = "dry_run"
        return resp

    # ------------------------------------------------------------------
    # READ tools (always allowed)
    # ------------------------------------------------------------------

    def get_task_by_id(self, task_id: str) -> ToolResponse:
        """Fetch a full Asana task by GID. Always allowed."""
        req = GetTaskByIdRequest(task_id=task_id)
        resp = self._client.call_tool("get_task_by_id", req.model_dump())
        resp.execution_mode = "live"
        return resp

    def get_comments(self, task_id: str) -> ToolResponse:
        """Fetch all comments (stories) on an Asana task. Always allowed."""
        req = GetCommentsRequest(task_id=task_id)
        resp = self._client.call_tool("get_comments", req.model_dump())
        resp.execution_mode = "live"
        return resp

    # ------------------------------------------------------------------
    # WRITE tools (blocked in dry-run)
    # ------------------------------------------------------------------

    def create_comment(
        self,
        task_id: str,
        text: str,
        is_pinned: bool = False,
    ) -> ToolResponse:
        """
        Post a comment to an Asana task.

        DRY_RUN=true  → returns simulated response, Asana is NOT called.
        DRY_RUN=false → posts real comment via MCP.
        """
        req = CreateCommentRequest(task_id=task_id, text=text, is_pinned=is_pinned)
        payload = req.model_dump()

        guarded = self._guard_write("create_comment", payload)
        if guarded is not None:
            return guarded

        resp = self._client.call_tool("create_comment", payload)
        resp.execution_mode = "live"
        return resp

    def update_task(
        self,
        task_id: str,
        fields: dict[str, Any],
    ) -> ToolResponse:
        """
        Update fields on an Asana task (e.g. assignee, due_on, tags).

        DRY_RUN=true  → returns simulated response, Asana is NOT called.
        DRY_RUN=false → updates real task via MCP.
        """
        req = UpdateTaskRequest(task_id=task_id, fields=fields)
        payload = req.model_dump()

        guarded = self._guard_write("update_task", payload)
        if guarded is not None:
            return guarded

        resp = self._client.call_tool("update_task", payload)
        resp.execution_mode = "live"
        return resp

    # ------------------------------------------------------------------
    # Generic passthrough (for extensibility)
    # ------------------------------------------------------------------

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> ToolResponse:
        """
        Generic tool call with guard enforcement.
        Read tools pass through; write tools are guarded.
        Unknown tool names are rejected.
        """
        if tool_name not in ALL_TOOLS:
            return ToolResponse(
                tool=tool_name,
                success=False,
                error=f"Unknown tool '{tool_name}'. Allowed: {sorted(ALL_TOOLS)}",
            )

        if tool_name in WRITE_TOOLS:
            guarded = self._guard_write(tool_name, arguments)
            if guarded is not None:
                return guarded

        return self._client.call_tool(tool_name, arguments)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_guarded_client(dry_run: Optional[bool] = None) -> GuardedMCPClient:
    """
    Create a GuardedMCPClient, reading DRY_RUN from settings if not provided.
    """
    if dry_run is None:
        from marketing_agent_engine.config.settings import settings
        dry_run = settings.dry_run
    return GuardedMCPClient(dry_run=dry_run)
