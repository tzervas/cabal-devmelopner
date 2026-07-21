"""Session JSONL recorder (E5.3).

Records agent runs to ``.cabal/runs/<task_id>.jsonl`` — one JSON object per
line. Every EventBus event is appended as it fires; the final structured answer
is appended via :meth:`SessionRecorder.record_final`. This gives an honest,
append-only, greppable trace of a run for later inspection / replay without any
external service.

Payloads are lightly redacted for common secret key names before write.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import Event, EventType

_SECRET_KEY = re.compile(
    r"(api[_-]?key|token|password|authorization|secret|bearer|xai_api_key|tero_tokens)",
    re.I,
)


def _safe_task_id(task_id: str) -> str:
    """Make a task id safe for use as a filename component."""
    cleaned = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in task_id)
    return cleaned or "run"


def _redact(obj: Any) -> Any:
    """Recursively redact values for secret-looking keys."""
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if _SECRET_KEY.search(str(k)):
                out[k] = "[redacted]"
            else:
                out[k] = _redact(v)
        return out
    if isinstance(obj, list):
        return [_redact(x) for x in obj]
    if isinstance(obj, str) and len(obj) > 12 and obj.startswith(("sk-", "xai-", "Bearer ")):
        return "[redacted]"
    return obj


class SessionRecorder:
    """Append run events + final answer to ``.cabal/runs/<task_id>.jsonl``."""

    def __init__(self, workspace_root: str | Path | None, task_id: str) -> None:
        root = Path(workspace_root) if workspace_root else Path.cwd()
        self.task_id = task_id
        runs_dir = root / ".cabal" / "runs"
        runs_dir.mkdir(parents=True, exist_ok=True)
        self.path = runs_dir / f"{_safe_task_id(task_id)}.jsonl"

    def _append(self, record: dict[str, Any]) -> None:
        safe = _redact(record)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(safe, default=str) + "\n")

    def record_event(self, event: Event) -> None:
        """Append one JSON line for an EventBus event."""
        self._append(
            {
                "ts": event.timestamp if event.timestamp is not None else time.time(),
                "type": str(event.type),
                "payload": event.payload,
            }
        )

    def record_final(self, structured_response_dict: dict[str, Any]) -> None:
        """Append the final structured answer line."""
        self._append(
            {
                "ts": time.time(),
                "type": "final",
                "payload": structured_response_dict,
            }
        )

    def attach(self, event_bus: EventBus) -> None:
        """Subscribe to every EventType so all events are recorded."""
        for event_type in EventType:
            event_bus.subscribe(event_type, self.record_event)
