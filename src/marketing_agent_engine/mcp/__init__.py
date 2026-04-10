"""
marketing_agent_engine.mcp

Public API for the MCP integration layer.
"""

from .client import MCPClient
from .guarded_client import DryRunViolationError, GuardedMCPClient, make_guarded_client
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

__all__ = [
    "MCPClient",
    "GuardedMCPClient",
    "DryRunViolationError",
    "make_guarded_client",
    "ToolResponse",
    "SimulatedWriteResponse",
    "GetTaskByIdRequest",
    "GetCommentsRequest",
    "CreateCommentRequest",
    "UpdateTaskRequest",
    "READ_TOOLS",
    "WRITE_TOOLS",
    "ALL_TOOLS",
]
