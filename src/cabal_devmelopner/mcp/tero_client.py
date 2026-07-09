"""Basic Tero-MCP client (PoC).

Talks to `tero-mcp-lite` over stdio JSON-RPC 2.0.

Default resolution (in priority):
1. TERO_INDEX_PATH / explicit index_path
2. Local repo docs/tero-index/index.json (walk up from cwd to find git root or use CWD)
3. Sibling layout fallback (for legacy mycelium-centric use; mycelium is isolated)

This makes any project with a committed docs/tero-index "ready" for cabal-devmelopner
when you run the agent inside (or pointed at) that project tree.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from cabal_devmelopner.core.schemas import Citation, StructuredResponse

# Sibling layout under ~/git (legacy)
_GIT_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_TERO_PROJECT = _GIT_ROOT / "tero-mcp"
_LEGACY_MYCELIUM_INDEX = _GIT_ROOT / "isolated" / "mycelium" / "docs" / "tero-index" / "index.json"
_DEFAULT_TOKEN = "local-dev"


def _find_local_tero_index(start: Path | None = None) -> Path | None:
    """Walk upward from start (or cwd) looking for a git repo with docs/tero-index/index.json."""
    p = (start or Path.cwd()).resolve()
    for _ in range(8):  # bound the walk
        cand = p / "docs" / "tero-index" / "index.json"
        if cand.is_file():
            return cand
        if (p / ".git").exists():
            # stop at git root even if no index here
            break
        parent = p.parent
        if parent == p:
            break
        p = parent
    return None


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
        env_index = os.environ.get("TERO_INDEX_PATH")
        explicit = Path(index_path) if index_path else None

        if explicit:
            index = explicit
        elif env_index:
            index = Path(env_index)
        else:
            local = _find_local_tero_index()
            index = local if local else _LEGACY_MYCELIUM_INDEX

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

    def text_search_structured(self, query: str, limit: int = 10) -> StructuredResponse:
        """StructuredResponse wrapper over text_search.

        Returns kind=answer (or refusal) with citations populated from tero.
        lang_refs / extended left for higher facade (mint) to fill for lang-docs + RAG.
        This is the schematized path used by agent orchestration for efficiency.
        """
        raw = self.text_search(query, limit=limit)
        if raw.get("kind") == "refusal" or "error" in raw:
            msg = raw.get("message") or raw.get("error") or "no citable results"
            return StructuredResponse.refusal(str(msg), extended={"raw": raw})

        items = raw.get("items") or []
        cits: list[Citation] = []
        for r in items:
            cits.append(
                Citation(
                    id=r.get("id") or r.get("anchor") or "unknown",
                    anchor=r.get("anchor"),
                    file=r.get("file"),
                    line=r.get("line"),
                    title=r.get("title"),
                    summary=r.get("summary"),
                    source="tero",
                )
            )

        answer_text = (
            "\n".join(
                f"[{c.id}] {c.title or ''}: {c.summary or ''} ({c.file or ''}:{c.line or ''})"
                for c in cits[:3]
            )
            or "See citations."
        )

        return StructuredResponse(
            kind="answer",
            answer=answer_text,
            citations=cits,
            explain=raw.get("explain"),
            extended={"raw": raw},
        )
