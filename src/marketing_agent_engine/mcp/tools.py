"""
Asana MCP tool interface definitions.

Defines the four tool contracts used by this system:
  - get_task_by_id   (READ)
  - get_comments     (READ)
  - create_comment   (WRITE — blocked in dry-run)
  - update_task      (WRITE — blocked in dry-run)

These are plain dataclasses / typed dicts — no MCP SDK dependency here.
The client is responsible for mapping these to actual MCP tool calls.
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Tool categories
# ---------------------------------------------------------------------------

READ_TOOLS: frozenset[str] = frozenset({"get_task_by_id", "get_comments"})
WRITE_TOOLS: frozenset[str] = frozenset({"create_comment", "update_task"})
ALL_TOOLS: frozenset[str] = READ_TOOLS | WRITE_TOOLS


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class GetTaskByIdRequest(BaseModel):
    task_id: str = Field(description="Asana task GID")


class GetCommentsRequest(BaseModel):
    task_id: str = Field(description="Asana task GID")


class CreateCommentRequest(BaseModel):
    task_id: str = Field(description="Asana task GID")
    text: str = Field(description="Comment body (plain text or HTML)")
    is_pinned: bool = Field(default=False, description="Pin comment to top of task")


class UpdateTaskRequest(BaseModel):
    task_id: str = Field(description="Asana task GID")
    fields: dict[str, Any] = Field(
        description="Dict of Asana task fields to update (e.g. assignee, due_on)"
    )


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class ToolResponse(BaseModel):
    tool: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    simulated: bool = False
    execution_mode: str = "live"


class SimulatedWriteResponse(BaseModel):
    simulated: Literal[True] = True
    execution_mode: Literal["dry_run"] = "dry_run"
    action: str
    payload: dict[str, Any]
    dry_run_note: str = (
        "DRY_RUN=true — this action was NOT executed against Asana."
    )

    def as_tool_response(self) -> ToolResponse:
        return ToolResponse(
            tool=self.action,
            success=True,
            data=self.model_dump(),
            simulated=True,
        )


class LiveWriteResponse(BaseModel):
    simulated: Literal[False] = False
    execution_mode: Literal["live"] = "live"
    tool: str
    data: Optional[Any] = None
