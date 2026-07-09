"""Prompt construction utilities for cabal-devmelopner.

Updated for workspace: dynamic tero (Rust-backed, categories, type hints), common memory
(tero + context-mcp + memory-gate-rs), local llama.cpp/GPU via providers, cross-repo
scoped knowledge, optimized context/token use, security-hardened tools (agent-mcp,
security-mcp, herr-doktor, webpuppet), single NL orchestration.

Now uses the accompanying Structured Prompt/Response schemas (see core/schemas.py)
for sectioned construction, reliable citations/lang_refs, and orchestration efficiency.
JSON Schema is the portable contract; this renders to text for current providers.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from cabal_devmelopner.core.schemas import MemoryContext, StructuredPrompt
from cabal_devmelopner.core.tools import get_tool_descriptions
from cabal_devmelopner.core.types import Task

SYSTEM_PROMPT = """You are an expert software engineering agent in a sophisticated multi-repo workspace.
Core capabilities (use them intelligently, scoped to relevance):
- Tero (dynamic from tero-rs binary): discover tools via categories (introspection, query, explain, maintenance). Always use tero__* or local tero-mcp-lite FIRST for cited, relevant context from any repo's index before grepping. Supports cross-repo: query relevant siblings if context matches the task (e.g., shared patterns in memory-gate or context-mcp). Use categories and schemas for smart calls; Python layer provides hints, Rust enforces validation.
- Common memory backend: tero for structured/cited L1, context-mcp for embeddings/RAG/session, memory-gate-rs for gated/consolidated/scoped memories with domains/tags. Tag/scope to current project; borrow/reuse from other repos ONLY if tero/context scores it highly relevant — avoid context bloat.
- Structured schemas (core/schemas.py): All memory injection and final outputs use StructuredPrompt / StructuredResponse. Required: kind + answer + citations. Optionals (for future + efficiency + orchestration): confidence, lang_refs (lang:rust-1.96 etc.), model, token_usage, orchestration (subtasks/delegation), extended.
- Local models: Prefer self-hosted llama.cpp / Ollama / local GPU (via providers or herr-doktor) for cost, privacy, speed. Use optimizations: small context windows, scoped retrieval, batch where possible, token-efficient prompts. Capable locals may receive response_format derived from the JSON schema.
- Tools & agents: Native MCPs (tero, context-mcp, agent-mcp for orchestration, security-mcp, webpuppet for research). Use via cabal or direct. Single NL interface to orchestrate across.
- Cross-repo: Tero indexes enable efficient knowledge transfer without loading full trees. Scope delivery to task-at-hand.
- Production principles: Security-hardened (auth, screening, gates), performance-optimized (local GPU, low token, fast retrieval), honest (citations, no silent failures).
- Workflow: Use Tero excavation first. Work on feature branches. PR to dev. Verify with checks, tero, tests.

Always cite sources, minimize tokens, scope context, prefer local efficient paths. Emit parseable citations + optional orchestration hints when relevant.
"""


def build_prompt(
    task: Task,
    feedback: Sequence[str] | None = None,
    extra_context: str | None = None,
) -> str:
    """
    Backward-compatible text prompt builder.

    New code should prefer build_structured_prompt (returns StructuredPrompt)
    which feeds .to_text() and carries typed memory_contexts / extended.
    """
    sp = build_structured_prompt(task, feedback=feedback, extra_context=extra_context)
    return sp.to_text()


def build_structured_prompt(
    task: Task,
    feedback: Sequence[str] | None = None,
    extra_context: str | None = None,
    memory_contexts: list[MemoryContext] | None = None,
    extended: dict[str, Any] | None = None,
) -> StructuredPrompt:
    """
    Build a StructuredPrompt (sectioned + schema-aware).

    Memory contexts (from tero + RAG + lang docs via domains) are carried typed.
    extra_context (legacy string) is wrapped as a single MemoryContext for compat.
    Use .to_text() for current providers; .to_dict() for structured-output or orch.
    The resulting prompt instructs models on StructuredResponse shape.
    """
    contexts: list[MemoryContext] = list(memory_contexts or [])

    if extra_context and not contexts:
        # Legacy path: wrap free-text (usually tero_client output) as one context.
        # In future facade this will be replaced by proper MemoryContext list.
        contexts.append(
            MemoryContext(
                source="tero",
                domain=None,
                items=[],
                citations=[],
                relevance=None,
                extended={"raw": extra_context[:2000]},
            )
        )

    system = SYSTEM_PROMPT.strip() + "\n\n" + get_tool_descriptions()
    return StructuredPrompt(
        system=system,
        task=task.description.strip(),
        memory_contexts=contexts,
        feedback=list(feedback or []),
        extended=extended,
    )
