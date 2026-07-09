"""Improved agent loop for cabal-devmelopner (PoC).

Now applies the structured prompt + response schemas for memory efficiency,
parseable citations/lang_refs from tero+RAG+lang-docs, and orchestration hooks.
"""

from __future__ import annotations

from typing import Any

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.prompt import build_structured_prompt
from cabal_devmelopner.core.schemas import MemoryContext, StructuredResponse
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
        """Run the agent loop. Returns raw text (compat). Prefer run_structured for schema use."""
        structured = self.run_structured(task)
        return structured.answer

    def run_structured(self, task: Task) -> StructuredResponse:
        """Run the agent loop returning a StructuredResponse.

        Uses StructuredPrompt internally (with memory_contexts for tero hits).
        Post-processes provider output into schema shape + extracts citations where possible.
        This makes downstream orchestration and memory use efficient + extensible.
        """
        self.event_bus.emit_simple(
            EventType.TASK_STARTED,
            task_id=task.id,
            description=task.description,
        )

        feedback: list[str] = []
        last_resp: StructuredResponse = StructuredResponse(kind="answer", answer="")

        for iteration in range(1, task.max_iterations + 1):
            self.event_bus.emit_simple(
                EventType.PROGRESS,
                message=f"Iteration {iteration}/{task.max_iterations}",
            )

            # Pull tero context as typed MemoryContext + StructuredResponse (schema path)
            mem_contexts = []
            if self.tero_client:
                try:
                    sresp = self.tero_client.text_search_structured(task.description, limit=5)
                    if not sresp.is_refusal() and sresp.citations:
                        mem_contexts.append(
                            MemoryContext(
                                source="tero",
                                citations=sresp.citations,
                                items=[],
                            )
                        )
                        last_resp = StructuredResponse(
                            kind="answer",
                            answer="",
                            citations=sresp.citations,
                            lang_refs=sresp.lang_refs,
                            explain=sresp.explain,
                        )
                except Exception as e:
                    # A2/POC-4: surface instead of silent pass; TUI/CLI listen for ERROR
                    self.event_bus.emit_simple(
                        EventType.ERROR,
                        error=f"Tero client error: {e}",
                        source="tero",
                        task_id=task.id,
                    )

            sp = build_structured_prompt(
                task,
                feedback=feedback,
                memory_contexts=mem_contexts or None,
                extended={"iteration": iteration},
            )
            prompt_text = sp.to_text()

            self.event_bus.emit_simple(EventType.GENERATION_STARTED)
            try:
                # Pass local-friendly options (temperature, max_tokens) if provider supports via **kwargs.
                # Structured providers can also receive format hints.
                call_kwargs: dict[str, Any] = {}
                if "local" in getattr(self.provider, "name", lambda: "")().lower():
                    call_kwargs.update({
                        "temperature": getattr(self.provider, "temperature", 0.2),
                        "max_tokens": getattr(self.provider, "max_tokens", 2048),
                    })
                raw = self.provider.complete(prompt_text, **call_kwargs)
            except Exception as e:
                # A2/POC-8: emit ERROR on provider failure (never silent); surface to UIs
                self.event_bus.emit_simple(
                    EventType.ERROR,
                    error=f"Provider error ({self.provider.name()}): {e}",
                    source="provider",
                    task_id=task.id,
                    iteration=iteration,
                )
                # Return error-shaped response for caller (keeps contract)
                self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
                return StructuredResponse(
                    kind="refusal",
                    answer=f"[error] Provider failed: {e}",
                    extended={"error": str(e)},
                )
            self.event_bus.emit_simple(
                EventType.GENERATION_COMPLETE,
                response_length=len(raw),
                iteration=iteration,
            )

            # Wrap into structured response (best-effort; real structured providers will improve)
            resp = StructuredResponse(
                kind="answer",
                answer=raw,
                citations=last_resp.citations,
                lang_refs=last_resp.lang_refs,
                model=(
                    getattr(self.provider, "name", lambda: None)()
                    if hasattr(self.provider, "name")
                    else None
                ),
                extended={"raw_prompt_len": len(prompt_text)},
            )

            last_resp = resp

            # PoC: first success. Real impl would verify + populate confidence/orchestration.
            if iteration == 1:
                self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
                return resp

            feedback.append("The previous attempt did not fully satisfy the requirements.")

        self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
        return last_resp
