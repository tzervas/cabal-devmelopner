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


def _is_safe_command(cmd: str) -> bool:
    """Basic allowlist + no dangerous patterns for MVP v0."""
    if not cmd or ";" in cmd or "&&" in cmd or "|" in cmd or ">" in cmd or "<" in cmd:
        return False
    try:
        argv = shlex.split(cmd)
    except Exception:
        return False
    if not argv:
        return False
    base = argv[0]
    # allow "python -m pytest" etc by checking first two tokens for common
    if base in SAFE_COMMANDS:
        return True
    if base in ("python", "python3") and len(argv) > 1 and argv[1] in ("-m", "-c"):
        return True
    return any(base.startswith(s) for s in SAFE_COMMANDS)


def parse_tool_call(text: str) -> ToolCall | None:
    """Parse a tool call from free-text model output (minimal format for PoC/MVP-1).

    Supported (exact-ish, case-insensitive name):
        call tool read_file with path is src/foo.py
        call tool list_dir with path is .
        call tool run_command with command is ls -l

    Falls back to None if no match (model gave final answer).
    """
    if not text:
        return None
    # find first plausible call
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
    # parse key is value pairs (simple, stop at next key)
    kv_re = re.finditer(r"(\w+)\s+is\s+([^\n]+?)(?=\s+\w+\s+is\s+|$)", rest)
    for kv in kv_re:
        k = kv.group(1).strip().lower()
        v = kv.group(2).strip()
        args[k] = v
    if not args:
        # fallback: treat whole rest as single arg by name
        if name == "read_file":
            args = {"path": rest}
        elif name == "list_dir":
            args = {"path": rest or "."}
        elif name == "run_command":
            args = {"command": rest}
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
    ) -> None:
        self.event_bus = event_bus or EventBus()
        self.root = Path(workspace_root or ".").resolve()
        self.max_bytes = max_bytes
        self.max_write_bytes = max_write_bytes
        self.timeout_sec = timeout_sec

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
        if not _is_safe_command(command):
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
AVAILABLE TOOLS (use EXACT format; one tool call per response unless finishing):
- read_file: read text (relative path under workspace)
  call tool read_file with path is src/example.py
- list_dir: list files/dirs (relative)
  call tool list_dir with path is .
- write_file: create/overwrite a text file under workspace (prefer apply_patch for edits)
  call tool write_file with path is src/foo.py content is print("hi")
- apply_patch: replace one exact unique snippet in a file (safer than full rewrite)
  call tool apply_patch with path is src/foo.py old is OLD_SNIPPET new is NEW_SNIPPET
- run_command: allowlisted verify/read cmds only (pytest/ruff/uv/python/git/ls/cat/head; no shell meta)
  call tool run_command with command is python -m pytest -q

After tool results, call another tool or give the final answer. Cite tero if used.
""".strip()
