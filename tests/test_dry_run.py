"""
test_dry_run.py — Safety tests for the MCP guard layer.

Ensures that DRY_RUN=true prevents any write reaching Asana,
read tools always pass through, and unknown tools are rejected cleanly.
"""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from marketing_agent_engine.mcp.guarded_client import GuardedMCPClient
from marketing_agent_engine.mcp.tools import (
    ALL_TOOLS,
    READ_TOOLS,
    WRITE_TOOLS,
    ToolResponse,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _mock_mcp(data: Any = None) -> MagicMock:
    m = MagicMock()
    m.connect.return_value = None
    m.disconnect.return_value = None
    m.call_tool.return_value = ToolResponse(
        tool="mock",
        success=True,
        data=data or {"result": "ok"},
        simulated=False,
        execution_mode="live",
    )
    return m


def _client(dry_run: bool, mock: MagicMock | None = None) -> GuardedMCPClient:
    return GuardedMCPClient(dry_run=dry_run, mcp_client=mock or _mock_mcp())


# ─────────────────────────────────────────────────────────────────────────────
# create_comment is NEVER executed in dry-run
# ─────────────────────────────────────────────────────────────────────────────

class TestCreateCommentDryRun:
    def test_returns_simulated_true(self) -> None:
        resp = _client(dry_run=True).create_comment("t1", "hello")
        assert resp.simulated is True

    def test_execution_mode_is_dry_run(self) -> None:
        resp = _client(dry_run=True).create_comment("t1", "hello")
        assert resp.execution_mode == "dry_run"

    def test_success_is_true(self) -> None:
        resp = _client(dry_run=True).create_comment("t1", "hello")
        assert resp.success is True

    def test_mcp_call_tool_never_called(self) -> None:
        mock = _mock_mcp()
        _client(dry_run=True, mock=mock).create_comment("t1", "hello")
        mock.call_tool.assert_not_called()

    def test_payload_task_id_preserved(self) -> None:
        resp = _client(dry_run=True).create_comment("task-999", "text", is_pinned=True)
        assert resp.data["payload"]["task_id"] == "task-999"

    def test_payload_text_preserved(self) -> None:
        resp = _client(dry_run=True).create_comment("t1", "My comment text")
        assert resp.data["payload"]["text"] == "My comment text"

    def test_dry_run_note_present(self) -> None:
        resp = _client(dry_run=True).create_comment("t1", "x")
        assert "DRY_RUN" in resp.data.get("dry_run_note", "")


# ─────────────────────────────────────────────────────────────────────────────
# update_task is NEVER executed in dry-run
# ─────────────────────────────────────────────────────────────────────────────

class TestUpdateTaskDryRun:
    def test_returns_simulated_true(self) -> None:
        resp = _client(dry_run=True).update_task("t2", {"assignee": "u001"})
        assert resp.simulated is True

    def test_execution_mode_is_dry_run(self) -> None:
        resp = _client(dry_run=True).update_task("t2", {"due_on": "2025-12-01"})
        assert resp.execution_mode == "dry_run"

    def test_mcp_call_tool_never_called(self) -> None:
        mock = _mock_mcp()
        _client(dry_run=True, mock=mock).update_task("t2", {"assignee": "u"})
        mock.call_tool.assert_not_called()

    def test_payload_task_id_preserved(self) -> None:
        resp = _client(dry_run=True).update_task("task-888", {"due_on": "2025-12-01"})
        assert resp.data["payload"]["task_id"] == "task-888"


# ─────────────────────────────────────────────────────────────────────────────
# Live mode calls reach MCP
# ─────────────────────────────────────────────────────────────────────────────

class TestLiveMode:
    def test_create_comment_live_calls_mcp(self) -> None:
        mock = _mock_mcp()
        c = _client(dry_run=False, mock=mock)
        c.connect()
        resp = c.create_comment("t3", "live comment")
        mock.call_tool.assert_called_once()
        assert resp.execution_mode == "live"
        c.disconnect()

    def test_update_task_live_calls_mcp(self) -> None:
        mock = _mock_mcp()
        c = _client(dry_run=False, mock=mock)
        c.connect()
        resp = c.update_task("t3", {"assignee": "u_new"})
        mock.call_tool.assert_called_once()
        assert resp.execution_mode == "live"
        c.disconnect()


# ─────────────────────────────────────────────────────────────────────────────
# Read tools always pass through regardless of dry_run
# ─────────────────────────────────────────────────────────────────────────────

class TestReadToolsPassThrough:
    def test_get_task_by_id_calls_mcp_in_dry_run(self) -> None:
        mock = _mock_mcp()
        c = _client(dry_run=True, mock=mock)
        c.connect()
        resp = c.get_task_by_id("t_read_1")
        mock.call_tool.assert_called_once_with("get_task_by_id", {"task_id": "t_read_1"})
        assert resp.execution_mode == "live"
        c.disconnect()

    def test_get_comments_calls_mcp_in_dry_run(self) -> None:
        mock = _mock_mcp()
        c = _client(dry_run=True, mock=mock)
        c.connect()
        c.get_comments("t_read_2")
        mock.call_tool.assert_called_once_with("get_comments", {"task_id": "t_read_2"})
        c.disconnect()

    def test_read_tool_response_not_simulated(self) -> None:
        mock = _mock_mcp()
        c = _client(dry_run=True, mock=mock)
        c.connect()
        resp = c.get_task_by_id("t_read_3")
        assert resp.simulated is False
        c.disconnect()


# ─────────────────────────────────────────────────────────────────────────────
# Tool set integrity
# ─────────────────────────────────────────────────────────────────────────────

class TestToolSets:
    def test_read_tools_contains_expected(self) -> None:
        assert "get_task_by_id" in READ_TOOLS
        assert "get_comments" in READ_TOOLS

    def test_write_tools_contains_expected(self) -> None:
        assert "create_comment" in WRITE_TOOLS
        assert "update_task" in WRITE_TOOLS

    def test_all_tools_is_union(self) -> None:
        assert ALL_TOOLS == READ_TOOLS | WRITE_TOOLS

    def test_read_write_disjoint(self) -> None:
        assert READ_TOOLS.isdisjoint(WRITE_TOOLS)

    def test_unknown_tool_returns_error_response(self) -> None:
        resp = _client(dry_run=False).call_tool("nonexistent_tool", {})
        assert resp.success is False
        assert "nonexistent_tool" in (resp.error or "")

    def test_unknown_tool_error_lists_allowed(self) -> None:
        resp = _client(dry_run=False).call_tool("bad_tool", {})
        assert resp.error is not None


# ─────────────────────────────────────────────────────────────────────────────
# Context manager lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestContextManager:
    def test_connect_and_disconnect_called(self) -> None:
        mock = _mock_mcp()
        with GuardedMCPClient(dry_run=False, mcp_client=mock):
            pass
        mock.connect.assert_called_once()
        mock.disconnect.assert_called_once()

    def test_returns_self_from_enter(self) -> None:
        mock = _mock_mcp()
        c = GuardedMCPClient(dry_run=True, mcp_client=mock)
        with c as ctx:
            assert ctx is c

    def test_dry_run_flag_readable(self) -> None:
        assert GuardedMCPClient(dry_run=True, mcp_client=_mock_mcp()).dry_run is True
        assert GuardedMCPClient(dry_run=False, mcp_client=_mock_mcp()).dry_run is False
