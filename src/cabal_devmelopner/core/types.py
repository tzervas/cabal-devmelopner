"""Core type definitions for cabal-devmelopner."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(str, Enum):
    """Types of events the agent can emit."""

    TASK_STARTED = "task_started"
    GENERATION_STARTED = "generation_started"
    GENERATION_COMPLETE = "generation_complete"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    PROGRESS = "progress"
    NEEDS_HUMAN_INPUT = "needs_human_input"
    ERROR = "error"
    TASK_COMPLETE = "task_complete"


@dataclass
class Event:
    """Base event emitted by the agent."""

    type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float | None = None


@dataclass
class Task:
    """Represents a unit of work for the agent."""

    id: str
    description: str
    context: dict[str, Any] = field(default_factory=dict)
    max_iterations: int = 5
