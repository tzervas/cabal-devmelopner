"""Basic smoke tests for cabal-devmelopner PoC."""

from cabal_devmelopner.core.agent import SimpleAgent
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
