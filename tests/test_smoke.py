"""Basic smoke tests for cabal-devmelopner PoC (expanded for A3)."""

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.events import EventBus, EventType
from cabal_devmelopner.core.types import Task
from cabal_devmelopner.providers.base import Provider


class MockProvider(Provider):
    """Simple mock provider for testing."""

    def __init__(self, response: str = "Mock response"):
        self.response = response
        self.call_count = 0

    def complete(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        return self.response

    def name(self) -> str:
        return "MockProvider"


def test_simple_agent_runs_once():
    """Basic smoke test that the agent can run a task."""
    provider = MockProvider(response="Test output")
    agent = SimpleAgent(provider=provider)

    task = Task(
        id="smoke-1",
        description="Test task",
        max_iterations=1,
    )

    result = agent.run(task)

    assert result == "Test output"
    assert provider.call_count == 1


def test_simple_agent_with_multiple_iterations():
    """Test that the agent respects max_iterations."""
    provider = MockProvider(response="Attempt output")
    agent = SimpleAgent(provider=provider)

    task = Task(
        id="smoke-2",
        description="Multi-iteration test",
        max_iterations=3,
    )

    result = agent.run(task)

    # With current PoC logic it returns on first success,
    # but we still want to ensure it doesn't crash with higher max_iterations.
    assert result == "Attempt output"


def test_eventbus_emits_and_subscribes():
    """A3: basic EventBus coverage (POC-7)."""
    bus = EventBus()
    seen = []

    def handler(ev):
        seen.append(ev.type)

    bus.subscribe(EventType.PROGRESS, handler)
    bus.emit_simple(EventType.PROGRESS, message="hi")
    assert EventType.PROGRESS in seen


def test_task_dataclass():
    """A3: Task is real dataclass not duck (ties to A1 POC-3)."""
    t = Task(id="t1", description="desc", max_iterations=2)
    assert t.id == "t1"
    assert t.max_iterations == 2
    assert isinstance(t.context, dict)


class FailingTeroClient:
    """Mock for Tero error path test."""

    def text_search_structured(self, query: str, limit: int = 5):
        raise RuntimeError("simulated tero mcp fail")


def test_tero_error_emits_event():
    """A3/A2: Tero failures surface via ERROR event, no silent pass (POC-4)."""
    provider = MockProvider("ok")
    bus = EventBus()
    errors = []

    def on_err(ev):
        errors.append(ev.payload)

    bus.subscribe(EventType.ERROR, on_err)
    agent = SimpleAgent(provider=provider, event_bus=bus, tero_client=FailingTeroClient())

    task = Task(id="e1", description="task with tero", max_iterations=1)
    _ = agent.run(task)

    assert len(errors) >= 1
    assert "Tero client error" in str(errors[0].get("error", ""))


def test_provider_error_emits_and_refusal():
    """A3/A2: provider failures emit ERROR + return refusal (POC-8)."""

    class BoomProvider(Provider):
        def complete(self, prompt: str, **kwargs):
            raise ValueError("boom provider")

        def name(self):
            return "Boom"

    bus = EventBus()
    errs = []
    bus.subscribe(EventType.ERROR, lambda e: errs.append(e.payload))
    agent = SimpleAgent(provider=BoomProvider(), event_bus=bus)

    task = Task(id="e2", description="will fail", max_iterations=1)
    resp = agent.run_structured(task)

    assert len(errs) >= 1
    assert "Provider error" in str(errs[0].get("error", ""))
    assert resp.kind == "refusal"
    assert "Provider failed" in resp.answer
