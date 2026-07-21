"""Minimal Tool host v0 for MVP-1 (B1 per plan.md + ROADMAP).

Implements: read_file, list_dir, run_command (allowlisted/safe).

Emits TOOL_CALL / TOOL_RESULT via EventBus.

Integrates with W2 StructuredResponse / agent loop (model proposes via text format, execute, re-prompt).

Security: fs ops confined to workspace_root; run_command allowlisted + no shell + timeout.
Tero-first for context; tools for acting on fs (read/list/verify). No arbitrary exec.

Cites: plan.md cabal-poc-mvp, ROADMAP Wave B B1/B2, types.py (pre-existing TOOL_*), AGENTS dev-workflow.
"""

from __future__ import annotations

import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import EventType


@dataclass
class ToolCall:
    """Parsed tool request from model output."""

    name: str
    args: dict[str, Any]


@dataclass
class ToolResult:
    """Result of tool execution (for feedback + events)."""

    name: str
    args: dict[str, Any]
    output: str
    success: bool


# Allowlist for run_command (prefix match on argv[0] or full for safety in MVP).
# Extend in config later (MVP-2). Read-only bias.
SAFE_COMMANDS = {
    "ls",
    "cat",
    "echo",
    "pwd",
    "head",
    "wc",
    "python",
    "python3",
    "ruff",
    "pytest",
    "uv",
}


def is_safe_command(cmd: str, allowlist: set[str] | frozenset[str] | None = None) -> bool:
    """Allowlist + no shell metacharacters. Basename of argv[0] must be allowlisted."""
    allowed = set(allowlist) if allowlist is not None else set(SAFE_COMMANDS)
    if not cmd or ";" in cmd or "&&" in cmd or "|" in cmd or ">" in cmd or "<" in cmd:
        return False
    if "`" in cmd or "$(" in cmd:
        return False
    try:
        argv = shlex.split(cmd)
    except Exception:
        return False
    if not argv:
        return False
    base = Path(argv[0]).name
    if base in allowed:
        return True
    if base in ("python", "python3") and len(argv) > 1 and argv[1] in ("-m", "-c"):
        return True
    # allow ./scripts/foo.sh only if bash/sh allowlisted and path is relative under workspace
    if base in ("bash", "sh") and len(argv) >= 2:
        script = argv[1]
        if not script.startswith("/") and ".." not in Path(script).parts:
            return True
    return False


def _is_safe_command(cmd: str) -> bool:
    """Backward-compatible default allowlist check."""
    return is_safe_command(cmd, SAFE_COMMANDS)


def _parse_json_tool_payload(obj: Any) -> ToolCall | None:
    """Accept common JSON shapes: {name, args|arguments|parameters}."""
    if not isinstance(obj, dict):
        return None
    name = obj.get("name") or obj.get("tool") or obj.get("tool_name")
    if not name:
        return None
    args = obj.get("args") or obj.get("arguments") or obj.get("parameters") or {}
    if not isinstance(args, dict):
        return None
    return ToolCall(name=str(name).strip().lower(), args=args)


def parse_tool_call(text: str) -> ToolCall | None:
    """Parse a tool call from model output (E1.2 multi-format).

    Supported (first match wins):
      1. Fenced JSON: ```json\\n{"name":"read_file","args":{"path":"x"}}\\n```
      2. Inline JSON object with name+args
      3. Legacy free-text: ``call tool read_file with path is src/foo.py``

    Falls back to None if no match (model gave final answer).
    """
    if not text:
        return None

    # 1) fenced json block
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        try:
            import json

            tc = _parse_json_tool_payload(json.loads(fence.group(1)))
            if tc:
                return tc
        except Exception:
            pass

    # 2) bare JSON object (brace-balanced scan for nested args)
    import json

    starts = [i for i, ch in enumerate(text) if ch == "{"]
    for start in starts:
        depth = 0
        for end in range(start, len(text)):
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
                if depth == 0:
                    snippet = text[start : end + 1]
                    try:
                        tc = _parse_json_tool_payload(json.loads(snippet))
                        if tc:
                            return tc
                    except Exception:
                        pass
                    break

    # 3) legacy free-text
    m = re.search(
        r"(?i)call\s+tool\s+(\w+)\s+with\s+(.+?)(?:\n|$)",
        text,
        re.DOTALL,
    )
    if not m:
        return None
    name = m.group(1).strip().lower()
    rest = m.group(2).strip()
    args: dict[str, Any] = {}
    kv_re = re.finditer(r"(\w+)\s+is\s+([^\n]+?)(?=\s+\w+\s+is\s+|$)", rest)
    for kv in kv_re:
        k = kv.group(1).strip().lower()
        v = kv.group(2).strip()
        args[k] = v
    if not args:
        if name == "read_file":
            args = {"path": rest}
        elif name == "list_dir":
            args = {"path": rest or "."}
        elif name == "run_command":
            args = {"command": rest}
        elif name in ("write_file", "apply_patch"):
            args = {"path": rest}
    return ToolCall(name=name, args=args)


class ToolHost:
    """Host for tools. Confined, evented, W2 compatible.

    v0 (MVP-1): read_file, list_dir, run_command
    v1 (1.0 E1): write_file, apply_patch (workspace-confined writes)
    """

    def __init__(
        self,
        event_bus: EventBus | None = None,
        workspace_root: str | Path | None = None,
        max_bytes: int = 16384,
        timeout_sec: int = 15,
        max_write_bytes: int = 256 * 1024,
        allowlist: set[str] | frozenset[str] | tuple[str, ...] | None = None,
    ) -> None:
        self.event_bus = event_bus or EventBus()
        self.root = Path(workspace_root or ".").resolve()
        self.max_bytes = max_bytes
        self.max_write_bytes = max_write_bytes
        self.timeout_sec = timeout_sec
        self.allowlist: set[str] = set(allowlist) if allowlist is not None else set(SAFE_COMMANDS)

    def _emit(self, etype: EventType, **payload: Any) -> None:
        self.event_bus.emit_simple(etype, **payload)

    def _resolve_in_workspace(self, path: str) -> Path | None:
        """Resolve relative path under root; None if escape / invalid."""
        if not path or path.startswith("/") or ".." in Path(path).parts:
            return None
        p = (self.root / path).resolve(strict=False)
        root_s = str(self.root)
        # Ensure path is under root (prefix + boundary)
        if p != self.root and not str(p).startswith(root_s + "/"):
            return None
        return p

    def read_file(self, path: str) -> str:
        """Read UTF8 text file (relative to root, size limited, no escape)."""
        self._emit(EventType.TOOL_CALL, name="read_file", args={"path": path})
        try:
            p = self._resolve_in_workspace(path)
            if p is None:
                out = f"[read_file error] path outside workspace or invalid: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="read_file",
                    args={"path": path},
                    output=out,
                    success=False,
                )
                return out
            if not p.is_file():
                out = f"[read_file error] not a file: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="read_file",
                    args={"path": path},
                    output=out,
                    success=False,
                )
                return out
            data = p.read_bytes()
            text = data[: self.max_bytes].decode("utf-8", errors="replace")
            if len(data) > self.max_bytes:
                text += f"\n... [truncated to {self.max_bytes} bytes]"
            self._emit(
                EventType.TOOL_RESULT,
                name="read_file",
                args={"path": path},
                output=text,
                success=True,
            )
            return text
        except Exception as e:
            out = f"[read_file error] {e}"
            self._emit(
                EventType.TOOL_RESULT,
                name="read_file",
                args={"path": path},
                output=out,
                success=False,
            )
            return out

    def list_dir(self, path: str = ".") -> str:
        """List directory entries (names only, no escape from root)."""
        self._emit(EventType.TOOL_CALL, name="list_dir", args={"path": path})
        try:
            p = self._resolve_in_workspace(path if path not in (".", "") else ".")
            if path in (".", ""):
                p = self.root
            elif p is None:
                out = f"[list_dir error] path outside workspace: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="list_dir",
                    args={"path": path},
                    output=out,
                    success=False,
                )
                return out
            if not p.is_dir():
                out = f"[list_dir error] not a dir: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="list_dir",
                    args={"path": path},
                    output=out,
                    success=False,
                )
                return out
            entries = []
            for e in sorted(p.iterdir())[:50]:  # cap for MVP
                kind = "d/" if e.is_dir() else "f/"
                entries.append(f"{kind}{e.name}")
            out = "\n".join(entries) or "(empty)"
            self._emit(
                EventType.TOOL_RESULT,
                name="list_dir",
                args={"path": path},
                output=out,
                success=True,
            )
            return out
        except Exception as e:
            out = f"[list_dir error] {e}"
            self._emit(
                EventType.TOOL_RESULT,
                name="list_dir",
                args={"path": path},
                output=out,
                success=False,
            )
            return out

    def run_command(self, command: str) -> str:
        """Run allowlisted command (no shell, timeout, capture stdout+stderr)."""
        self._emit(EventType.TOOL_CALL, name="run_command", args={"command": command})
        if not is_safe_command(command, self.allowlist):
            out = f"[run_command error] command not in allowlist or unsafe pattern: {command[:80]}"
            self._emit(
                EventType.TOOL_RESULT,
                name="run_command",
                args={"command": command},
                output=out,
                success=False,
            )
            return out
        try:
            argv = shlex.split(command)
            proc = subprocess.run(
                argv,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                shell=False,
            )
            out = (proc.stdout or "") + (proc.stderr or "")
            if proc.returncode != 0:
                out = f"[exit {proc.returncode}] " + out
            out = out[: self.max_bytes]
            self._emit(
                EventType.TOOL_RESULT,
                name="run_command",
                args={"command": command},
                output=out,
                success=(proc.returncode == 0),
            )
            return out
        except subprocess.TimeoutExpired:
            out = "[run_command error] timed out"
            self._emit(
                EventType.TOOL_RESULT,
                name="run_command",
                args={"command": command},
                output=out,
                success=False,
            )
            return out
        except Exception as e:
            out = f"[run_command error] {e}"
            self._emit(
                EventType.TOOL_RESULT,
                name="run_command",
                args={"command": command},
                output=out,
                success=False,
            )
            return out

    def write_file(self, path: str, content: str) -> str:
        """Write UTF-8 text under workspace (create parents). No escape; size capped."""
        args = {"path": path, "bytes": len(content.encode("utf-8"))}
        self._emit(EventType.TOOL_CALL, name="write_file", args=args)
        try:
            p = self._resolve_in_workspace(path)
            if p is None:
                out = f"[write_file error] path outside workspace or invalid: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="write_file",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            raw = content.encode("utf-8")
            if len(raw) > self.max_write_bytes:
                out = (
                    f"[write_file error] content exceeds max_write_bytes="
                    f"{self.max_write_bytes} ({len(raw)} bytes)"
                )
                self._emit(
                    EventType.TOOL_RESULT,
                    name="write_file",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            # Refuse writing outside text-ish safety: block path traversal already done;
            # also refuse writing into .git
            if ".git" in p.parts:
                out = "[write_file error] writing under .git is not allowed"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="write_file",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
            out = f"wrote {len(raw)} bytes to {path}"
            self._emit(
                EventType.TOOL_RESULT,
                name="write_file",
                args=args,
                output=out,
                success=True,
            )
            return out
        except Exception as e:
            out = f"[write_file error] {e}"
            self._emit(
                EventType.TOOL_RESULT,
                name="write_file",
                args=args,
                output=out,
                success=False,
            )
            return out

    def apply_patch(self, path: str, old: str, new: str) -> str:
        """Replace first exact occurrence of old with new in a workspace file.

        Safer than full rewrite when the model can quote a unique snippet.
        """
        args = {"path": path, "old_len": len(old), "new_len": len(new)}
        self._emit(EventType.TOOL_CALL, name="apply_patch", args=args)
        try:
            p = self._resolve_in_workspace(path)
            if p is None:
                out = f"[apply_patch error] path outside workspace or invalid: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            if not p.is_file():
                out = f"[apply_patch error] not a file: {path}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            if ".git" in p.parts:
                out = "[apply_patch error] writing under .git is not allowed"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            text = p.read_text(encoding="utf-8")
            if old not in text:
                out = "[apply_patch error] old snippet not found (must match exactly once region)"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            if text.count(old) > 1:
                out = (
                    "[apply_patch error] old snippet matches multiple times; "
                    "use a longer unique context or write_file"
                )
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            updated = text.replace(old, new, 1)
            raw = updated.encode("utf-8")
            if len(raw) > self.max_write_bytes:
                out = f"[apply_patch error] result exceeds max_write_bytes={self.max_write_bytes}"
                self._emit(
                    EventType.TOOL_RESULT,
                    name="apply_patch",
                    args=args,
                    output=out,
                    success=False,
                )
                return out
            p.write_bytes(raw)
            out = f"patched {path} ({len(old)} → {len(new)} chars)"
            self._emit(
                EventType.TOOL_RESULT,
                name="apply_patch",
                args=args,
                output=out,
                success=True,
            )
            return out
        except Exception as e:
            out = f"[apply_patch error] {e}"
            self._emit(
                EventType.TOOL_RESULT,
                name="apply_patch",
                args=args,
                output=out,
                success=False,
            )
            return out

    def execute(self, name: str, args: dict[str, Any]) -> ToolResult:
        """Dispatch by name. Returns ToolResult (events already emitted)."""
        name = name.lower()
        if name == "read_file":
            path = args.get("path") or args.get("file") or "."
            output = self.read_file(str(path))
            return ToolResult(
                name=name, args={"path": path}, output=output, success=not output.startswith("[")
            )
        if name == "list_dir":
            path = args.get("path") or "."
            output = self.list_dir(str(path))
            return ToolResult(
                name=name, args={"path": path}, output=output, success=not output.startswith("[")
            )
        if name == "run_command":
            cmd = args.get("command") or args.get("cmd") or ""
            output = self.run_command(str(cmd))
            return ToolResult(
                name=name, args={"command": cmd}, output=output, success=not output.startswith("[")
            )
        if name == "write_file":
            path = args.get("path") or args.get("file") or ""
            content = args.get("content") or args.get("text") or ""
            output = self.write_file(str(path), str(content))
            return ToolResult(
                name=name,
                args={"path": path},
                output=output,
                success=not output.startswith("["),
            )
        if name == "apply_patch":
            path = args.get("path") or args.get("file") or ""
            old = args.get("old") or args.get("search") or ""
            new = args.get("new") or args.get("replace") or ""
            output = self.apply_patch(str(path), str(old), str(new))
            return ToolResult(
                name=name,
                args={"path": path},
                output=output,
                success=not output.startswith("["),
            )
        # unknown
        out = f"[tool error] unknown tool: {name}"
        self._emit(EventType.TOOL_RESULT, name=name, args=args, output=out, success=False)
        return ToolResult(name=name, args=args, output=out, success=False)


def get_tool_descriptions() -> str:
    """Text block for injection into StructuredPrompt / system for model to learn format."""
    return """
AVAILABLE TOOLS (one tool call per response unless finishing). Prefer fenced JSON:

```json
{"name": "read_file", "args": {"path": "src/example.py"}}
```

Legacy free-text also works:
  call tool read_file with path is src/example.py
  call tool list_dir with path is .
  call tool write_file with path is src/foo.py content is print("hi")
  call tool apply_patch with path is src/foo.py old is OLD_SNIPPET new is NEW_SNIPPET
  call tool run_command with command is python -m pytest -q

Tools: read_file, list_dir, write_file, apply_patch, run_command (allowlisted only).
After tool results, call another tool or give the final answer. Cite tero if used.
""".strip()
