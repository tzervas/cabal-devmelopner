"""Improved agent loop for cabal-devmelopner (PoC).

Now applies the structured prompt + response schemas for memory efficiency,
parseable citations/lang_refs from tero+RAG+lang-docs, and orchestration hooks.
"""

from __future__ import annotations

from typing import Any

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.prompt import build_structured_prompt
from cabal_devmelopner.core.schemas import (
    AgentDomain,
    CommonMemoryAdapter,
    MemoryContext,
    StructuredResponse,
)
from cabal_devmelopner.core.tools import ToolHost, parse_tool_call
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.base import Provider


class SimpleAgent:
    """
    PoC/MVP-1 agent with loop + W2 Structured + tero facade + minimal tools (B1/B2).

    Tools opt-in: model proposes (text format) -> execute (read/list/run allowlist) via ToolHost
    emitting TOOL_CALL/RESULT, feedback re-prompt limited steps. Integrates tero/W2.
    """

    def __init__(
        self,
        provider: Provider,
        event_bus: EventBus | None = None,
        tero_client: TeroMCPClient | None = None,
        tools_enabled: bool = False,
        workspace_root: str | None = None,
    ) -> None:
        self.provider = provider
        self.event_bus = event_bus or EventBus()
        self.tero_client = tero_client
        self.facade: CommonMemoryAdapter | None = (
            CommonMemoryAdapter(tero_client) if tero_client else None
        )
        self.tools_enabled = tools_enabled
        self.tool_host: ToolHost | None = (
            ToolHost(event_bus=self.event_bus, workspace_root=workspace_root)
            if tools_enabled
            else None
        )
        self._tool_steps = 0
        self._max_tool_steps = 4  # MVP-1 budget (B2)

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
        self._tool_steps = 0
        last_resp: StructuredResponse = StructuredResponse(kind="answer", answer="")

        for iteration in range(1, task.max_iterations + 1):
            self.event_bus.emit_simple(
                EventType.PROGRESS,
                message=f"Iteration {iteration}/{task.max_iterations}",
            )

            # Pull via W2 CommonMemory facade (domain TERO) -- full integration.
            # Domain-scoped, always StructuredResponse + citations. Legacy fallback kept.
            mem_contexts = []
            sresp: StructuredResponse | None = None
            if getattr(self, "facade", None):
                try:
                    sresp = self.facade.query(AgentDomain.TERO, task.description, {"limit": 5})
                    if sresp and sresp.is_refusal():
                        # C0 honesty (never-silent) + POC-4/A3: even though facade returns explicit
                        # StructuredResponse.refusal on backend error (per its contract), the agent
                        # (which owns the EventBus) MUST emit ERROR so UIs/logs/observers see it.
                        # This makes tero/facade failures visible; no silent refusal path.
                        err_msg = (
                            (sresp.extended or {}).get("error") or sresp.answer or "facade refusal"
                        )
                        self.event_bus.emit_simple(
                            EventType.ERROR,
                            error=f"CommonMemory facade error: {err_msg}",
                            source="facade",
                            task_id=task.id,
                        )
                    elif not sresp.is_refusal() and sresp.citations:
                        mem_contexts.append(
                            MemoryContext(
                                source="tero",
                                domain=AgentDomain.TERO.value,
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
                            extended={"facade_domain": AgentDomain.TERO.value},
                        )
                except Exception as e:
                    # A2/POC-8 + C0 honesty: surface errors, never silent
                    self.event_bus.emit_simple(
                        EventType.ERROR,
                        error=f"CommonMemory facade error: {e}",
                        source="facade",
                        task_id=task.id,
                    )
            elif self.tero_client and not getattr(self, "facade", None):
                # legacy direct (compat during transition to facade; unreachable if tero_client passed
                # because __init__ sets facade=CommonMemoryAdapter(tero_client) )
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
                    call_kwargs.update(
                        {
                            "temperature": getattr(self.provider, "temperature", 0.2),
                            "max_tokens": getattr(self.provider, "max_tokens", 2048),
                        }
                    )
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

            # MVP-1 tool loop (B2): if model emitted a tool call format, execute (host emits TOOL_*),
            # feed result back via feedback, re-prompt (limited steps). Integrates tero/W2 (prompt has context).
            # When tools disabled (default for compat), or no tool call, treat as final answer (old PoC path).
            if getattr(self, "tools_enabled", False) and getattr(self, "tool_host", None):
                tc = parse_tool_call(raw)
                if tc:
                    self._tool_steps = getattr(self, "_tool_steps", 0) + 1
                    if self._tool_steps > getattr(self, "_max_tool_steps", 4):
                        feedback.append(
                            "Tool step budget exceeded. Provide final answer based on context."
                        )
                    else:
                        tres = self.tool_host.execute(tc.name, tc.args)
                        feedback.append(
                            f"TOOL RESULT {tres.name} args={tres.args}: success={tres.success}\n{tres.output[:700]}"
                        )
                        # re-prompt with tool feedback (model decides next tool or answer)
                        continue

            # Final answer path:
            # - tools off: single-shot (honest PoC default) after first completion
            # - tools on: return when model gave a direct answer (no tool call this turn)
            if not getattr(self, "tools_enabled", False):
                self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
                return resp
            # tools enabled + no tool call this iteration → treat as final answer
            self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
            return resp

        self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
        return last_resp
