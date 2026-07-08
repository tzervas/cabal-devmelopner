"""Event system following a simple producer/consumer model."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from cabal_devmelopner.core.types import Event, EventType


class EventBus:
    """
    Simple event bus for producer/consumer style communication.

    The core agent produces events. Different consumers (CLI, TUI, future Discord, etc.)
    can subscribe to events they care about.
    """

    def __init__(self) -> None:
        self._subscribers: dict[EventType, list[Callable[[Event], None]]] = {}

    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """Subscribe a handler to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def emit(self, event_type: EventType, payload: dict[str, Any] | None = None) -> None:
        """Emit an event to all subscribed handlers."""
        event = Event(
            type=event_type,
            payload=payload or {},
            timestamp=time.time(),
        )
        for handler in self._subscribers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                # In PoC we print; in production this should be logged properly
                print(f"[EventBus] Handler error for {event_type}: {e}")

    def emit_simple(self, event_type: EventType, **kwargs: Any) -> None:
        """Convenience method to emit an event with keyword arguments as payload."""
        self.emit(event_type, payload=kwargs)
