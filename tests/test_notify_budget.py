"""E7.1 notify + E3.2 wall budget tests."""

from __future__ import annotations

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.config import parse_config_data
from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.notify import NullNotifier, RelayNotifier, resolve_relay_script
from cabal_devmelopner.providers.base import Provider


class SlowProvider(Provider):
    def __init__(self):
        self.n = 0

    def complete(self, prompt: str, **kwargs) -> str:
        self.n += 1
        import time

        time.sleep(0.05)
        return f"tick {self.n}"

    def name(self) -> str:
        return "slow"


class AlwaysToolProvider(Provider):
    """Keeps calling tools so the agent loop iterates (budget checked each iter)."""

    def complete(self, prompt: str, **kwargs) -> str:
        import time

        time.sleep(0.04)
        return "call tool list_dir with path is ."

    def name(self) -> str:
        return "always-tool"


def test_wall_budget_stops_loop(tmp_path):
    bus = EventBus()
    errs = []
    bus.subscribe(EventType.ERROR, lambda e: errs.append(e.payload))
    agent = SimpleAgent(
        provider=AlwaysToolProvider(),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        max_wall_secs=0.1,
        use_verify=False,
        max_tool_steps=50,
    )
    resp = agent.run_structured(Task(id="b1", description="slow", max_iterations=40))
    assert any(e.get("source") == "budget" for e in errs)
    assert "budget" in resp.answer or (resp.extended or {}).get("budget")


def test_null_notifier():
    assert NullNotifier().notify("hi") is False


def test_relay_notifier_missing_script(tmp_path):
    bus = EventBus()
    errs = []
    bus.subscribe(EventType.ERROR, lambda e: errs.append(e.payload))
    n = RelayNotifier(script=tmp_path / "nope.sh", event_bus=bus, enabled=True)
    assert n.notify("hello") is False
    assert errs


def test_relay_notifier_runs_script(tmp_path):
    script = tmp_path / "relay-notify.sh"
    script.write_text("#!/bin/sh\necho ok\n")
    script.chmod(0o755)
    n = RelayNotifier(script=script, enabled=True)
    assert n.notify("status ping", label="test") is True


def test_notify_config_parse():
    cfg = parse_config_data(
        {
            "agent": {"max_wall_secs": 120},
            "notify": {"enabled": True, "label": "x"},
        }
    )
    assert cfg.max_wall_secs == 120.0
    assert cfg.notify.enabled is True
    assert cfg.notify.label == "x"


def test_resolve_relay_optional():
    # may or may not find install; must not crash
    _ = resolve_relay_script()
