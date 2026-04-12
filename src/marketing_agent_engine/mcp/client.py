"""
Asana REST API client.

Replaces the previous MCP stdio subprocess with direct Asana REST API calls
via httpx. This eliminates the Node.js/npx dependency entirely.

Environment variables required:
  ASANA_PERSONAL_ACCESS_TOKEN  — PAT for authentication

The client is intentionally thin — it performs no dry-run logic.
Dry-run enforcement is the responsibility of GuardedMCPClient.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

import httpx

from .tools import ToolResponse

logger = logging.getLogger(__name__)

ASANA_API_BASE = "https://app.asana.com/api/1.0"


class MCPClient:
    """
    Direct Asana REST API client.

    Usage:
        client = MCPClient()
        result = client.call_tool("create_comment", {"task_id": "123", "text": "hello"})

    Or as context manager (no-op connect/disconnect for API compatibility):
        with MCPClient() as client:
            result = client.call_tool("get_task_by_id", {"task_id": "123"})
    """

    def __init__(self, **_kwargs: Any) -> None:
        self._pat = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
        self._request_id = 0

    def _headers(self) -> dict[str, str]:
        if not self._pat:
            raise RuntimeError("ASANA_PERSONAL_ACCESS_TOKEN not set")
        return {
            "Authorization": f"Bearer {self._pat}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # Lifecycle (no-op, kept for API compatibility)
    # ------------------------------------------------------------------

    def connect(self) -> None:
        logger.info("Asana REST API client ready (PAT=%s...)", self._pat[:8] if self._pat else "NONE")

    def disconnect(self) -> None:
        pass

    def __enter__(self) -> "MCPClient":
        self.connect()
        return self

    def __exit__(self, *_: Any) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # Tool dispatch
    # ------------------------------------------------------------------

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> ToolResponse:
        dispatch = {
            "get_task_by_id": self._get_task_by_id,
            "get_comments": self._get_comments,
            "create_comment": self._create_comment,
            "update_task": self._update_task,
        }
        handler = dispatch.get(tool_name)
        if handler is None:
            return ToolResponse(
                tool=tool_name,
                success=False,
                error=f"Unknown tool '{tool_name}'. Allowed: {sorted(dispatch)}",
            )
        try:
            return handler(arguments)
        except Exception as exc:
            logger.error("Asana API error calling %s: %s", tool_name, exc)
            return ToolResponse(tool=tool_name, success=False, error=str(exc))

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    def _get_task_by_id(self, args: dict[str, Any]) -> ToolResponse:
        task_id = args.get("task_id", "")
        url = f"{ASANA_API_BASE}/tasks/{task_id}"
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=self._headers())
            resp.raise_for_status()
            return ToolResponse(tool="get_task_by_id", success=True, data=resp.json().get("data", {}))

    def _get_comments(self, args: dict[str, Any]) -> ToolResponse:
        task_id = args.get("task_id", "")
        url = f"{ASANA_API_BASE}/tasks/{task_id}/stories"
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=self._headers())
            resp.raise_for_status()
            return ToolResponse(tool="get_comments", success=True, data=resp.json().get("data", []))

    def _create_comment(self, args: dict[str, Any]) -> ToolResponse:
        task_id = args.get("task_id", "")
        text = args.get("text", "")
        is_pinned = args.get("is_pinned", False)
        url = f"{ASANA_API_BASE}/tasks/{task_id}/stories"
        body = {"data": {"text": text, "is_pinned": is_pinned}}
        logger.info("Posting comment to task %s (%d chars, pinned=%s)", task_id, len(text), is_pinned)
        with httpx.Client(timeout=15) as client:
            resp = client.post(url, headers=self._headers(), json=body)
            resp.raise_for_status()
            data = resp.json().get("data", {})
            logger.info("Comment created: story_gid=%s", data.get("gid", "unknown"))
            return ToolResponse(tool="create_comment", success=True, data=data)

    def _update_task(self, args: dict[str, Any]) -> ToolResponse:
        task_id = args.get("task_id", "")
        fields = args.get("fields", {})
        url = f"{ASANA_API_BASE}/tasks/{task_id}"
        body = {"data": fields}
        with httpx.Client(timeout=15) as client:
            resp = client.put(url, headers=self._headers(), json=body)
            resp.raise_for_status()
            return ToolResponse(tool="update_task", success=True, data=resp.json().get("data", {}))
