"""E6.2 cancel + E7.3 HITL write approval tests."""

from __future__ import annotations

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.config import parse_config_data
from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.providers.base import Provider


class AlwaysToolProvider(Provider):
    def complete(self, prompt: str, **kwargs) -> str:
        return "call tool list_dir with path is ."

    def name(self) -> str:
        return "always-tool"


class WriteOnceProvider(Provider):
    def __init__(self) -> None:
        self.n = 0

    def complete(self, prompt: str, **kwargs) -> str:
        self.n += 1
        if self.n == 1:
            return (
                'call tool write_file with path is hello.txt content is "hi"\n'
                # also support JSON path if free-text fails — free-text should work
            )
        return "done after tool"

    def name(self) -> str:
        return "write-once"


def test_cancel_stops_loop(tmp_path):
    bus = EventBus()
    errs: list[dict] = []
    bus.subscribe(EventType.ERROR, lambda e: errs.append(e.payload))
    agent = SimpleAgent(
        provider=AlwaysToolProvider(),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        use_verify=False,
        max_tool_steps=50,
    )
    agent.request_cancel()
    resp = agent.run_structured(Task(id="c1", description="go", max_iterations=20))
    assert any(e.get("source") == "cancel" for e in errs)
    assert (resp.extended or {}).get("cancelled") is True
    assert "cancelled" in resp.answer


def test_hitl_denies_write_without_callback(tmp_path):
    bus = EventBus()
    hitl: list[dict] = []
    bus.subscribe(EventType.NEEDS_HUMAN_INPUT, lambda e: hitl.append(e.payload))
    agent = SimpleAgent(
        provider=WriteOnceProvider(),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        use_verify=False,
        require_write_approval=True,
        approval_callback=None,
        max_tool_steps=5,
    )
    agent.run_structured(Task(id="h1", description="write", max_iterations=3))
    assert hitl
    assert hitl[0].get("tool") == "write_file"
    assert not (tmp_path / "hello.txt").exists()


def test_hitl_approves_write(tmp_path):
    bus = EventBus()
    agent = SimpleAgent(
        provider=WriteOnceProvider(),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        use_verify=False,
        require_write_approval=True,
        approval_callback=lambda _n, _a: True,
        max_tool_steps=5,
    )
    agent.run_structured(Task(id="h2", description="write", max_iterations=3))
    assert (tmp_path / "hello.txt").is_file()
    # free-text tool parser may keep surrounding quotes
    assert (tmp_path / "hello.txt").read_text().strip('"') == "hi"


def test_require_write_approval_config():
    cfg = parse_config_data({"tools": {"require_write_approval": True}})
    assert cfg.tools.require_write_approval is True
