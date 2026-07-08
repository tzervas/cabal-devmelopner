"""Functional TUI for cabal-devmelopner (PoC).

This version allows running tasks directly from the TUI with live event output.
"""

from __future__ import annotations

import os

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, RichLog, Static

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.events import Event, EventBus, EventType
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.xai import XaiProvider


class CabalDevmelopnerTUI(App):
    """PoC TUI that can actually run the agent."""

    CSS = """
    Screen {
        background: #1a1a1a;
    }
    #title {
        text-style: bold;
        padding: 1;
    }
    #log {
        height: 1fr;
        border: solid #444;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.log_widget = RichLog(highlight=True, markup=True, wrap=True)
        self.input_widget = Input(placeholder="Enter your task here...", id="task_input")
        self.run_button = Button("Run Task", variant="primary", id="run_button")
        self.event_bus: EventBus | None = None
        self.agent: SimpleAgent | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("cabal-devmelopner — PoC TUI", id="title")
        yield Vertical(
            self.input_widget,
            self.run_button,
            self.log_widget,
            id="main_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.log_widget.write("[dim]Ready. Enter a task and press Run.[/]")
        self.input_widget.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run_button":
            self._run_task()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "task_input":
            self._run_task()

    def _run_task(self) -> None:
        task_text = self.input_widget.value.strip()
        if not task_text:
            self.log_widget.write("[red]Please enter a task description.[/]")
            return

        self.log_widget.clear()
        self.log_widget.write(f"[bold yellow]Starting task:[/] {task_text}\n")

        self.event_bus = EventBus()
        self._subscribe_to_events()

        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            self.log_widget.write("[bold red]Error: XAI_API_KEY not set in environment.[/]")
            return

        try:
            provider = XaiProvider(api_key=api_key)
            tero_client = TeroMCPClient() if os.getenv("USE_TERO", "false").lower() == "true" else None

            self.agent = SimpleAgent(
                provider=provider,
                event_bus=self.event_bus,
                tero_client=tero_client
            )

            self.run_worker(self._execute_agent, task_text, thread=True)

        except Exception as e:
            self.log_widget.write(f"[bold red]Failed to initialize agent:[/] {e}")

    def _subscribe_to_events(self) -> None:
        if not self.event_bus:
            return
        self.event_bus.subscribe(EventType.PROGRESS, self._on_progress)
        self.event_bus.subscribe(EventType.GENERATION_STARTED, self._on_generation_started)
        self.event_bus.subscribe(EventType.GENERATION_COMPLETE, self._on_generation_complete)
        self.event_bus.subscribe(EventType.TASK_COMPLETE, self._on_task_complete)
        self.event_bus.subscribe(EventType.ERROR, self._on_error)

    def _execute_agent(self, task_description: str) -> None:
        if not self.agent:
            return
        try:
            task = type("Task", (), {
                "id": "tui-task",
                "description": task_description,
                "max_iterations": 3
            })()
            result = self.agent.run(task)
            self.call_from_thread(
                self.log_widget.write,
                f"\n[bold green]=== Final Result ===[/]\n{result}"
            )
        except Exception as e:
            self.call_from_thread(
                self.log_widget.write,
                f"[bold red]Agent error:[/] {e}"
            )

    def _on_progress(self, event: Event) -> None:
        msg = event.payload.get("message", "")
        self.call_from_thread(self.log_widget.write, f"[cyan]▶[/] {msg}")

    def _on_generation_started(self, event: Event) -> None:
        self.call_from_thread(self.log_widget.write, "[yellow]Generating response...[/]")

    def _on_generation_complete(self, event: Event) -> None:
        length = event.payload.get("response_length", 0)
        self.call_from_thread(self.log_widget.write, f"[green]✓ Generation complete ({length} chars)[/]")

    def _on_task_complete(self, event: Event) -> None:
        self.call_from_thread(self.log_widget.write, "[bold green]Task finished.[/]")

    def _on_error(self, event: Event) -> None:
        err = event.payload.get("error", "Unknown error")
        self.call_from_thread(self.log_widget.write, f"[bold red]Error:[/] {err}")