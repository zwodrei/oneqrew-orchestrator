"""
Asana MCP stdio client.

Wraps the Asana MCP server that runs as a child process over stdio.
Communicates using the MCP JSON-RPC protocol (tools/call).

Environment variables required:
  ASANA_MCP_APP_CLIENT_ID      — Asana OAuth App Client ID
  ASANA_MCP_APP_CLIENT_SECRET  — Asana OAuth App Client Secret
  ASANA_PERSONAL_ACCESS_TOKEN  — PAT (alternative to OAuth flow)

The client is intentionally thin — it performs no dry-run logic.
Dry-run enforcement is the responsibility of GuardedMCPClient.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from typing import Any, Optional

from .tools import ToolResponse

logger = logging.getLogger(__name__)

# Asana MCP OAuth credentials (injected from env or module-level defaults)
_DEFAULT_CLIENT_ID = os.getenv("ASANA_MCP_APP_CLIENT_ID", "1213962784022453")
_DEFAULT_CLIENT_SECRET = os.getenv(
    "ASANA_MCP_APP_CLIENT_SECRET", "ba579b66e93c4947fe30e0f529c88d16"
)


class MCPClient:
    """
    Minimal stdio-based MCP client for the Asana MCP server.

    Usage:
        client = MCPClient()
        client.connect()
        result = client.call_tool("get_task_by_id", {"task_id": "123"})
        client.disconnect()

    Or as context manager:
        with MCPClient() as client:
            result = client.call_tool("get_task_by_id", {"task_id": "123"})
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        pat: Optional[str] = None,
        server_command: Optional[list[str]] = None,
    ) -> None:
        self._client_id = client_id or _DEFAULT_CLIENT_ID
        self._client_secret = client_secret or _DEFAULT_CLIENT_SECRET
        self._pat = pat or os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
        self._server_command = server_command or self._default_server_command()
        self._process: Optional[subprocess.Popen] = None  # type: ignore[type-arg]
        self._request_id = 0

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _default_server_command(self) -> list[str]:
        """
        Default command to start the Asana MCP server over stdio.
        Resolves npx from PATH (or common locations on Railway/Nix).
        """
        npx_path = shutil.which("npx")
        if npx_path is None:
            for candidate in ["/usr/local/bin/npx", "/usr/bin/npx", "/.nix-profile/bin/npx"]:
                if os.path.isfile(candidate):
                    npx_path = candidate
                    break
        if npx_path is None:
            npx_path = "npx"
        cmd = [npx_path, "-y", "@asana/mcp"]
        if self._pat:
            cmd += ["--token", self._pat]
        return cmd

    def connect(self) -> None:
        if self._process is not None:
            return
        logger.debug("Starting Asana MCP server: %s", self._server_command)
        env = {
            **os.environ,
            "ASANA_CLIENT_ID": self._client_id,
            "ASANA_CLIENT_SECRET": self._client_secret,
        }
        if self._pat:
            env["ASANA_TOKEN"] = self._pat

        try:
            self._process = subprocess.Popen(
                self._server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
            )
        except FileNotFoundError:
            logger.error(
                "MCP server command not found: %s. "
                "Ensure Node.js/npx is installed (required for Asana MCP). "
                "On Railway, add a Node.js buildpack or set DRY_RUN=true.",
                self._server_command[0],
            )
            raise RuntimeError(
                f"Cannot start Asana MCP server: '{self._server_command[0]}' not found. "
                f"Install Node.js or set DRY_RUN=true."
            ) from None
        logger.info("Asana MCP server started (pid=%s)", self._process.pid)

    def disconnect(self) -> None:
        if self._process is None:
            return
        try:
            self._process.stdin.close()  # type: ignore[union-attr]
            self._process.wait(timeout=5)
        except Exception:
            self._process.kill()
        finally:
            self._process = None
            logger.info("Asana MCP server stopped.")

    def __enter__(self) -> "MCPClient":
        self.connect()
        return self

    def __exit__(self, *_: Any) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # RPC
    # ------------------------------------------------------------------

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a JSON-RPC request and return the parsed response."""
        if self._process is None or self._process.stdin is None:
            raise RuntimeError("MCPClient is not connected. Call connect() first.")

        line = json.dumps(payload) + "\n"
        logger.debug("MCP → %s", line.rstrip())
        self._process.stdin.write(line)
        self._process.stdin.flush()

        response_line = self._process.stdout.readline()  # type: ignore[union-attr]
        logger.debug("MCP ← %s", response_line.rstrip())

        if not response_line:
            stderr = self._process.stderr.read() if self._process.stderr else ""
            raise RuntimeError(f"MCP server closed stdout. stderr: {stderr}")

        return json.loads(response_line)

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> ToolResponse:
        """
        Call an MCP tool by name with the given arguments.
        Returns a ToolResponse; never raises on tool-level errors (wraps them).
        """
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        try:
            raw = self._send(payload)
        except Exception as exc:
            logger.error("MCP transport error calling %s: %s", tool_name, exc)
            return ToolResponse(tool=tool_name, success=False, error=str(exc))

        if "error" in raw:
            err = raw["error"]
            logger.warning("MCP tool error for %s: %s", tool_name, err)
            return ToolResponse(
                tool=tool_name,
                success=False,
                error=str(err.get("message", err)) if isinstance(err, dict) else str(err),
            )

        result = raw.get("result", {})
        content = result.get("content", result)
        return ToolResponse(tool=tool_name, success=True, data=content)
