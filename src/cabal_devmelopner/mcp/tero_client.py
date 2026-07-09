"""Basic Tero-MCP client (PoC).

Talks to `tero-mcp-lite` over stdio JSON-RPC 2.0. Defaults point at the sibling
checkout at `../tero-mcp` and the Mycelium corpus index at
`../mycelium/docs/tero-index/index.json` (override via env / constructor args).
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

# Sibling layout under ~/git: cabal-devmelopner | tero-mcp | mycelium
_GIT_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_TERO_PROJECT = _GIT_ROOT / "tero-mcp"
_DEFAULT_INDEX = _GIT_ROOT / "mycelium" / "docs" / "tero-index" / "index.json"
_DEFAULT_TOKEN = "local-dev"


class TeroMCPClient:
    """Minimal stdio client for tero-mcp-lite (one request per process)."""

    def __init__(
        self,
        command: list[str] | None = None,
        *,
        index_path: str | Path | None = None,
        token: str | None = None,
        project_path: str | Path | None = None,
    ) -> None:
        project = Path(project_path or os.environ.get("TERO_MCP_PROJECT") or _DEFAULT_TERO_PROJECT)
        index = Path(index_path or os.environ.get("TERO_INDEX_PATH") or _DEFAULT_INDEX)
        self.token = token or os.environ.get("TERO_TOKEN") or _DEFAULT_TOKEN
        self.env = {
            **os.environ,
            "TERO_TOKENS": os.environ.get("TERO_TOKENS", f"{self.token}:refresh"),
            "TERO_INDEX_PATH": str(index),
        }
        self.command = command or [
            "uv",
            "run",
            "--project",
            str(project),
            "tero-mcp-lite",
            "--index",
            str(index),
        ]

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call a tool on the Tero-MCP server (one-shot stdio)."""
        args = {**arguments}
        args.setdefault("token", self.token)
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args,
            },
        }

        try:
            proc = subprocess.run(
                self.command,
                input=json.dumps(request) + "\n",
                capture_output=True,
                text=True,
                timeout=45,
                env=self.env,
            )
            if proc.returncode != 0:
                stderr = (proc.stderr or "").strip()
                return {"error": f"Tero-MCP exited with code {proc.returncode}: {stderr[:300]}"}

            stdout = (proc.stdout or "").strip()
            if not stdout:
                return {"error": "Tero-MCP returned empty response"}

            # Server may emit multiple NDJSON lines; take the last complete object.
            line = stdout.splitlines()[-1]
            response = json.loads(line)
            if "error" in response:
                return {"error": response["error"]}

            result = response.get("result", response)
            return self._unwrap_tool_result(result)
        except subprocess.TimeoutExpired:
            return {"error": "Tero-MCP request timed out"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse Tero-MCP response: {e}"}
        except Exception as e:
            return {"error": f"Tero-MCP client error: {e}"}

    @staticmethod
    def _unwrap_tool_result(result: dict[str, Any]) -> dict[str, Any]:
        """Parse MCP tool content envelope into the Tero answer/refusal payload."""
        if result.get("isError"):
            return {"error": result}

        content = result.get("content")
        if isinstance(content, list) and content:
            text = content[0].get("text") if isinstance(content[0], dict) else None
            if isinstance(text, str):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"raw": text}

        return result

    def text_search(self, query: str, limit: int = 10) -> dict[str, Any]:
        """Ranked free-text search over id/title/summary."""
        # Server API uses `value`; limit is applied client-side (server caps at 20).
        payload = self.call_tool("text_search", {"value": query})
        if "error" in payload or payload.get("kind") == "refusal":
            return payload
        items = payload.get("items") or []
        if limit and len(items) > limit:
            payload = {**payload, "items": items[:limit]}
        return payload

    def query_by_id(self, value: str) -> dict[str, Any]:
        return self.call_tool("query_by_id", {"value": value})

    def identify(self) -> dict[str, Any]:
        return self.call_tool("identify", {})
