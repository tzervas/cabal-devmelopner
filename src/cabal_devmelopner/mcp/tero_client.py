"""Basic Tero-MCP client (PoC stub).

This is a minimal client for interacting with a Tero-MCP server over stdio.
It will be expanded significantly once we have a proper MCP client framework.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any


class TeroMCPClient:
    """
    Very basic Tero-MCP client for PoC.

    In later versions this will be replaced with a proper MCP client that can
    discover tools, handle authentication, and integrate cleanly with the agent.
    """

    def __init__(self, command: list[str] | None = None) -> None:
        # Default assumes `tero-mcp-lite` is available in PATH or via uv
        self.command = command or ["uv", "run", "--project", "packages/tero-mcp-lite", "tero-mcp-lite"]

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call a tool on the Tero-MCP server (very naive stdio implementation)."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        try:
            proc = subprocess.run(
                self.command,
                input=json.dumps(request).encode(),
                capture_output=True,
                timeout=45,
            )
            if proc.returncode != 0:
                stderr = proc.stderr.decode(errors="ignore").strip()
                return {"error": f"Tero-MCP exited with code {proc.returncode}: {stderr[:300]}"}

            stdout = proc.stdout.decode(errors="ignore").strip()
            if not stdout:
                return {"error": "Tero-MCP returned empty response"}

            response = json.loads(stdout)
            return response.get("result", response)
        except subprocess.TimeoutExpired:
            return {"error": "Tero-MCP request timed out"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse Tero-MCP response: {e}"}
        except Exception as e:
            return {"error": f"Tero-MCP client error: {e}"}

    def text_search(self, query: str, limit: int = 10) -> dict[str, Any]:
        """Simple wrapper around text_search tool."""
        return self.call_tool("text_search", {"query": query, "limit": limit})
