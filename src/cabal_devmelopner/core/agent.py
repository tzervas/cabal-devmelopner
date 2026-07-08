"""Improved agent loop for cabal-devmelopner (PoC)."""

from __future__ import annotations

from typing import Any

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.prompt import build_prompt
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.base import Provider


class SimpleAgent:
    """
    PoC agent with a proper while-loop and feedback support.

    This version supports multiple iterations with feedback from previous attempts.
    It is still simple but forms a solid foundation for later expansion
    (Tero-MCP context, tool use, swarm coordination, etc.).
    """

    def __init__(
        self,
        provider: Provider,
        event_bus: EventBus | None = None,
        tero_client: TeroMCPClient | None = None,
    ) -> None:
        self.provider = provider
        self.event_bus = event_bus or EventBus()
        self.tero_client = tero_client

    def run(self, task: Task) -> str:
        """Run the agent loop on a task with iteration and feedback."""
        self.event_bus.emit_simple(
            EventType.TASK_STARTED,
            task_id=task.id,
            description=task.description,
        )

        feedback: list[str] = []
        last_response = ""

        for iteration in range(1, task.max_iterations + 1):
            self.event_bus.emit_simple(
                EventType.PROGRESS,
                message=f"Iteration {iteration}/{task.max_iterations}",
            )

            # Pull relevant context from Tero if available (PoC level)
            tero_context = ""
            if self.tero_client:
                try:
                    search_result = self.tero_client.text_search(task.description, limit=5)
                    if "results" in search_result:
                        tero_context = "\n".join(
                            f"- {r.get('title', '')}: {r.get('summary', '')}"
                            for r in search_result["results"][:3]
                        )
                except Exception:
                    pass  # Fail gracefully in PoC

            prompt = build_prompt(task, feedback=feedback, extra_context=tero_context)

            self.event_bus.emit_simple(EventType.GENERATION_STARTED)
            response = self.provider.complete(prompt)
            self.event_bus.emit_simple(
                EventType.GENERATION_COMPLETE,
                response_length=len(response),
                iteration=iteration,
            )

            last_response = response

            # TODO: In real versions we would run verification here and collect real feedback.
            # For PoC we treat the first generation as success.
            if iteration == 1:
                self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
                return response

            feedback.append("The previous attempt did not fully satisfy the requirements.")

        self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
        return last_response
