"""Tests for the E5.3 session JSONL recorder."""

import json

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.session import SessionRecorder
from cabal_devmelopner.core.types import EventType


def _read_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_recorder_creates_jsonl_under_runs(tmp_path):
    """SessionRecorder creates .cabal/runs/<task_id>.jsonl."""
    rec = SessionRecorder(tmp_path, "task-1")
    assert rec.path == tmp_path / ".cabal" / "runs" / "task-1.jsonl"
    assert rec.path.parent.is_dir()


def test_attach_records_events_and_final(tmp_path):
    """Attaching to a bus records each event as a JSON line; final is appended."""
    bus = EventBus()
    rec = SessionRecorder(tmp_path, "task-2")
    rec.attach(bus)

    bus.emit_simple(EventType.TASK_STARTED, task_id="task-2", description="hi")
    bus.emit_simple(EventType.PROGRESS, message="working")
    rec.record_final({"kind": "answer", "answer": "done"})

    lines = _read_lines(rec.path)
    assert len(lines) == 3
    assert lines[0]["type"] == str(EventType.TASK_STARTED)
    assert lines[0]["payload"]["description"] == "hi"
    assert lines[1]["type"] == str(EventType.PROGRESS)
    assert lines[-1]["type"] == "final"
    assert lines[-1]["payload"]["answer"] == "done"
    # every line carries a timestamp
    assert all(line.get("ts") is not None for line in lines)


def test_record_event_appends(tmp_path):
    """record_event appends one line per call (append-only)."""
    from cabal_devmelopner.core.types import Event

    rec = SessionRecorder(tmp_path, "task-3")
    rec.record_event(Event(type=EventType.ERROR, payload={"error": "boom"}, timestamp=1.0))
    rec.record_event(Event(type=EventType.TASK_COMPLETE, payload={}, timestamp=2.0))

    lines = _read_lines(rec.path)
    assert len(lines) == 2
    assert lines[0]["ts"] == 1.0
    assert lines[0]["payload"]["error"] == "boom"


def test_unsafe_task_id_sanitized(tmp_path):
    """A task id with path separators does not escape the runs dir."""
    rec = SessionRecorder(tmp_path, "a/b c")
    assert rec.path.parent == tmp_path / ".cabal" / "runs"
    rec.record_final({"kind": "answer", "answer": "ok"})
    assert rec.path.is_file()
