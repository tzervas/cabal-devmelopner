"""Minimal TUI for cabal-devmelopner (PoC).

This is a very basic Textual app to demonstrate the direction.
It will be significantly expanded in the MVP phase.
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static

from cabal_devmelopner.core.events import EventBus, Event, EventType


class CabalDevmelopnerTUI(App):
    """Basic TUI application for cabal-devmelopner PoC."""

    CSS = """
    Screen {
        background: #1a1a1a;
    }
    """

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__()
        self.event_bus = event_bus
        self.log_widget = RichLog(highlight=True, markup=True)

        # Subscribe to events
        self.event_bus.subscribe(EventType.PROGRESS, self.on_progress)
        self.event_bus.subscribe(EventType.GENERATION_COMPLETE, self.on_generation_complete)
        self.event_bus.subscribe(EventType.TASK_COMPLETE, self.on_task_complete)
        self.event_bus.subscribe(EventType.ERROR, self.on_error)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("cabal-devmelopner — PoC TUI", id="title")
        yield self.log_widget
        yield Footer()

    def on_progress(self, event: Event) -> None:
        message = event.payload.get("message", "")
        self.log_widget.write(f"[cyan]▶[/] {message}")

    def on_generation_complete(self, event: Event) -> None:
        length = event.payload.get("response_length", 0)
        self.log_widget.write(f"[green]✓[/] Generation complete ({length} chars)")

    def on_task_complete(self, event: Event) -> None:
        self.log_widget.write("[bold green]Task completed successfully.[/]")

    def on_error(self, event: Event) -> None:
        error = event.payload.get("error", "Unknown error")
        self.log_widget.write(f"[bold red]Error:[/] {error}")

    def run_agent(self, task_description: str) -> None:
        """Placeholder — in a real version this would run the agent in a worker."""
        self.log_widget.write(f"[yellow]Starting task:[/] {task_description}")
        # TODO: Integrate actual agent execution here (run in worker thread)
        self.log_widget.write("[dim]Agent execution not yet wired into TUI (PoC).[/]")
