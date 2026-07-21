"""Functional TUI for cabal-devmelopner (E6.1 dogfood surface).

Run tasks with live EventBus log: progress, tools, verify, errors, session path.
"""

from __future__ import annotations

import os
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, RichLog, Static

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.config import load_config
from cabal_devmelopner.core.events import Event, EventBus
from cabal_devmelopner.core.session import SessionRecorder
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.base import LocalOllamaProvider, Provider
from cabal_devmelopner.providers.xai import XaiProvider


class CabalDevmelopnerTUI(App):
    """Leaf-agent TUI with live event log (E6.1)."""

    CSS = """
    Screen {
        background: #1a1a1a;
    }
    #title {
        text-style: bold;
        padding: 1;
    }
    #status {
        color: #aaa;
        padding: 0 1;
    }
    #log {
        height: 1fr;
        border: solid #444;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.log_widget = RichLog(highlight=True, markup=True, wrap=True, id="log")
        self.input_widget = Input(placeholder="Enter your task here...", id="task_input")
        self.run_button = Button("Run Task", variant="primary", id="run_button")
        self.status = Static("", id="status")
        self.event_bus: EventBus | None = None
        self.agent: SimpleAgent | None = None
        self.recorder: SessionRecorder | None = None
        self.cfg = load_config()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("cabal-devmelopner — TUI (tools / verify / session)", id="title")
        yield self.status
        yield Vertical(self.input_widget, self.run_button, self.log_widget, id="main_container")
        yield Footer()

    def on_mount(self) -> None:
        self.status.update(
            f"profile={self.cfg.profile.name} provider={self.cfg.profile.provider} "
            f"tools={self.cfg.use_tools} verify={self.cfg.use_verify}"
        )
        self.log_widget.write("[dim]Ready. Enter a task and press Run (Enter works).[/]")
        self.input_widget.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run_button":
            self._run_task()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "task_input":
            self._run_task()

    def _make_provider(self) -> Provider:
        name = self.cfg.profile.provider
        if name == "xai":
            api_key = os.getenv("XAI_API_KEY")
            if not api_key:
                self.log_widget.write("[yellow]XAI_API_KEY unset — falling back to local-ollama[/]")
                name = "local-ollama"
            else:
                return XaiProvider(api_key=api_key, model=self.cfg.profile.model or "grok-4.5")
        return LocalOllamaProvider(
            model=self.cfg.profile.local_model or self.cfg.profile.model or "llama3.2",
            temperature=self.cfg.profile.temperature,
            max_tokens=self.cfg.profile.max_tokens,
        )

    def _run_task(self) -> None:
        task_text = self.input_widget.value.strip()
        if not task_text:
            self.log_widget.write("[red]Please enter a task description.[/]")
            return

        self.log_widget.clear()
        self.log_widget.write(f"[bold yellow]Starting task:[/] {task_text}\n")

        self.event_bus = EventBus()
        self._subscribe_to_events()

        task = Task(
            id=f"tui-{abs(hash(task_text)) % 10_000_000}",
            description=task_text,
            max_iterations=self.cfg.max_iterations,
        )
        self.recorder = SessionRecorder(self.cfg.workspace_root or ".", task.id)
        self.recorder.attach(self.event_bus)

        try:
            provider = self._make_provider()
            if self.cfg.tero.mcp_project:
                os.environ.setdefault("TERO_MCP_PROJECT", self.cfg.tero.mcp_project)
            if self.cfg.tero.index_path:
                os.environ.setdefault("TERO_INDEX_PATH", self.cfg.tero.index_path)
            tero_client = TeroMCPClient() if self.cfg.profile.use_tero else None
            self.agent = SimpleAgent(
                provider=provider,
                event_bus=self.event_bus,
                tero_client=tero_client,
                tools_enabled=self.cfg.use_tools,
                workspace_root=self.cfg.workspace_root,
                max_tool_steps=self.cfg.max_tool_steps,
                verify_command=self.cfg.tools.verify_command if self.cfg.use_verify else None,
                max_verify_rounds=self.cfg.tools.max_verify_rounds,
                use_verify=self.cfg.use_verify and self.cfg.use_tools,
                command_allowlist=self.cfg.tools.allowlist,
            )
            self.log_widget.write(
                f"[dim]session → {self.recorder.path} · provider={provider.name()}[/]\n"
            )
            self.run_worker(self._execute_agent, task, thread=True)
        except Exception as e:
            self.log_widget.write(f"[bold red]Failed to initialize agent:[/] {e}")

    def _subscribe_to_events(self) -> None:
        if not self.event_bus:
            return
        bus = self.event_bus
        bus.subscribe(EventType.PROGRESS, self._on_progress)
        bus.subscribe(EventType.GENERATION_STARTED, self._on_generation_started)
        bus.subscribe(EventType.GENERATION_COMPLETE, self._on_generation_complete)
        bus.subscribe(EventType.TASK_COMPLETE, self._on_task_complete)
        bus.subscribe(EventType.ERROR, self._on_error)
        bus.subscribe(EventType.TOOL_CALL, self._on_tool_call)
        bus.subscribe(EventType.TOOL_RESULT, self._on_tool_result)
        bus.subscribe(EventType.VERIFY_STARTED, self._on_verify_started)
        bus.subscribe(EventType.VERIFY_RESULT, self._on_verify_result)

    def _execute_agent(self, task: Task) -> None:
        if not self.agent:
            return
        try:
            structured = self.agent.run_structured(task)
            if self.recorder:
                try:
                    self.recorder.record_final(structured.to_dict())
                except Exception:
                    self.recorder.record_final(
                        {"answer": structured.answer, "kind": structured.kind}
                    )
            self.call_from_thread(
                self.log_widget.write,
                f"\n[bold green]=== Final ({structured.kind}) ===[/]\n{structured.answer}",
            )
            if self.recorder:
                self.call_from_thread(
                    self.log_widget.write,
                    f"\n[dim]session recorded → {self.recorder.path}[/]",
                )
        except Exception as e:
            self.call_from_thread(self.log_widget.write, f"[bold red]Agent error:[/] {e}")

    def _on_progress(self, event: Event) -> None:
        msg = event.payload.get("message", "")
        self.call_from_thread(self.log_widget.write, f"[cyan]▶[/] {msg}")

    def _on_generation_started(self, event: Event) -> None:
        self.call_from_thread(self.log_widget.write, "[yellow]Generating…[/]")

    def _on_generation_complete(self, event: Event) -> None:
        length = event.payload.get("response_length", 0)
        self.call_from_thread(
            self.log_widget.write, f"[green]✓ generation complete ({length} chars)[/]"
        )

    def _on_task_complete(self, event: Event) -> None:
        self.call_from_thread(self.log_widget.write, "[bold green]Task finished.[/]")

    def _on_error(self, event: Event) -> None:
        err = event.payload.get("error", "Unknown error")
        hint = event.payload.get("hint")
        line = f"[bold red]Error:[/] {err}"
        if hint:
            line += f"\n[dim]hint: {hint}[/]"
        self.call_from_thread(self.log_widget.write, line)

    def _on_tool_call(self, event: Event) -> None:
        name = event.payload.get("name")
        args = event.payload.get("args")
        self.call_from_thread(self.log_widget.write, f"[magenta]TOOL_CALL[/] {name} {args}")

    def _on_tool_result(self, event: Event) -> None:
        name = event.payload.get("name")
        ok = event.payload.get("success")
        out = str(event.payload.get("output", ""))[:160]
        color = "green" if ok else "red"
        self.call_from_thread(
            self.log_widget.write, f"[{color}]TOOL_RESULT[/] {name} success={ok}: {out}"
        )

    def _on_verify_started(self, event: Event) -> None:
        cmd = event.payload.get("command")
        rnd = event.payload.get("round", 0)
        self.call_from_thread(self.log_widget.write, f"[blue]VERIFY start[/] round={rnd}: {cmd}")

    def _on_verify_result(self, event: Event) -> None:
        ok = event.payload.get("success")
        out = str(event.payload.get("output", ""))[:160]
        color = "green" if ok else "red"
        self.call_from_thread(
            self.log_widget.write, f"[{color}]VERIFY {'ok' if ok else 'FAIL'}[/]: {out}"
        )


def main() -> None:
    """Entrypoint for `cabal-devmelopner-tui` console script (A1/POC-1)."""
    # Ensure workspace cwd is used for config search
    Path.cwd()
    app = CabalDevmelopnerTUI()
    app.run()


if __name__ == "__main__":
    main()
