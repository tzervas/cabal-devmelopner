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


def _verify_output_ok(vout: str) -> bool:
    """True when ToolHost.run_command reports success (no error/exit prefix)."""
    if not vout:
        return True
    if vout.startswith("[exit ") or vout.startswith("[run_command error]"):
        return False
    # other tool-style bracket errors
    return not (vout.startswith("[") and "error" in vout[:40].lower())


class SimpleAgent:
    """
    PoC/MVP-1 agent with loop + W2 Structured + tero facade + minimal tools (B1/B2).

    Tools opt-in: model proposes (text format) -> execute (read/list/run allowlist) via ToolHost
    emitting TOOL_CALL/RESULT, feedback re-prompt limited steps. Integrates tero/W2.

    E2 verify: when tools are on and the model stops calling tools, optionally run
    ``verify_command`` and re-prompt up to ``max_verify_rounds`` on failure.
    """

    def __init__(
        self,
        provider: Provider,
        event_bus: EventBus | None = None,
        tero_client: TeroMCPClient | None = None,
        tools_enabled: bool = False,
        workspace_root: str | None = None,
        *,
        max_tool_steps: int = 5,
        verify_command: str | None = None,
        max_verify_rounds: int = 2,
        use_verify: bool = True,
        command_allowlist: tuple[str, ...] | None = None,
    ) -> None:
        self.provider = provider
        self.event_bus = event_bus or EventBus()
        self.tero_client = tero_client
        self.facade: CommonMemoryAdapter | None = (
            CommonMemoryAdapter(tero_client) if tero_client else None
        )
        self.tools_enabled = tools_enabled
        self.tool_host: ToolHost | None = (
            ToolHost(
                event_bus=self.event_bus,
                workspace_root=workspace_root,
                allowlist=command_allowlist,
            )
            if tools_enabled
            else None
        )
        self._tool_steps = 0
        self._max_tool_steps = max(1, max_tool_steps)
        self.verify_command = verify_command
        self.max_verify_rounds = max(0, max_verify_rounds)
        self.use_verify = use_verify and bool(verify_command)
        self._verify_rounds = 0

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
        self._verify_rounds = 0
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
            if self.tools_enabled and self.tool_host:
                tc = parse_tool_call(raw)
                if tc:
                    self._tool_steps += 1
                    if self._tool_steps > self._max_tool_steps:
                        feedback.append(
                            "Tool step budget exceeded. Provide final answer based on context."
                        )
                        # re-prompt so the model can give a real final answer (not a tool call)
                        continue
                    tres = self.tool_host.execute(tc.name, tc.args)
                    feedback.append(
                        f"TOOL RESULT {tres.name} args={tres.args}: success={tres.success}\n"
                        f"{tres.output[:700]}"
                    )
                    # re-prompt with tool feedback (model decides next tool or answer)
                    continue

            # Final answer path:
            # - tools off: single-shot (honest PoC default) after first completion
            # - tools on: when model stops calling tools, optionally run verify (E2)
            if not self.tools_enabled:
                self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
                return resp

            verified, retry_note = self._run_verify(task, resp)
            if verified is not None:
                return verified
            if retry_note:
                feedback.append(retry_note)
            continue

        self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
        return last_resp

    def _run_verify(
        self,
        task: Task,
        resp: StructuredResponse,
    ) -> tuple[StructuredResponse | None, str | None]:
        """Run configured verify_command after a tools-path final answer (E2).

        Returns:
          (StructuredResponse, None) — finish the task (pass, exhausted rounds, or disabled)
          (None, feedback_str) — verify failed with rounds left; continue the agent loop
        """
        if not self.use_verify or not self.verify_command or not self.tool_host:
            self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
            return resp, None

        cmd = self.verify_command
        self.event_bus.emit_simple(
            EventType.VERIFY_STARTED,
            command=cmd,
            task_id=task.id,
            round=self._verify_rounds,
        )
        vout = self.tool_host.run_command(cmd)
        ok = _verify_output_ok(vout)
        self.event_bus.emit_simple(
            EventType.VERIFY_RESULT,
            command=cmd,
            success=ok,
            output=vout[:1500],
            task_id=task.id,
            round=self._verify_rounds,
        )

        if ok:
            self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
            return (
                StructuredResponse(
                    kind=resp.kind,
                    answer=resp.answer,
                    citations=resp.citations,
                    lang_refs=resp.lang_refs,
                    model=resp.model,
                    explain=resp.explain,
                    extended={
                        **(resp.extended or {}),
                        "verify": {"ok": True, "command": cmd, "output": vout[:500]},
                    },
                ),
                None,
            )

        self._verify_rounds += 1
        if self._verify_rounds > self.max_verify_rounds:
            self.event_bus.emit_simple(
                EventType.ERROR,
                error=f"verify failed after {self.max_verify_rounds} round(s): {cmd}",
                source="verify",
                task_id=task.id,
            )
            self.event_bus.emit_simple(EventType.TASK_COMPLETE, task_id=task.id)
            return (
                StructuredResponse(
                    kind="answer",
                    answer=(
                        (resp.answer or "")
                        + f"\n\n[verify FAILED after {self.max_verify_rounds} rounds]\n"
                        + vout[:800]
                    ),
                    citations=resp.citations,
                    extended={
                        **(resp.extended or {}),
                        "verify": {"ok": False, "command": cmd, "output": vout[:800]},
                    },
                ),
                None,
            )

        note = (
            f"VERIFY FAILED ({cmd}):\n{vout[:700]}\n"
            "Fix the failures with tools, then give a final answer again."
        )
        return None, note
