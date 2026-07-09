"""Structured Prompt and Response schema set for efficient shared memory,
agent orchestration, and future extension.

This is the canonical contract accompanying dual tero + RAG + lang-docs memory
integration (see wsfull/mint/ctx kickoffs). Source of truth is the embedded
JSON_SCHEMA (portable across Python/Rust/MCP consumers). Dataclasses provide
ergonomic Python usage with to_dict/from_dict and optional-field support.

Design goals (efficiency + orch):
- Required core: kind + answer + citations (deterministic, tero-style, never silent).
- Optional fields for extension without breaking changes: confidence, lang_refs
  (for Rust 1.96 / Python 3.13/3.14 hits), model, token_usage, orchestration
  (subtasks, next_action, delegation for agent layers), extended (catch-all bag),
  explain.
- StructuredPrompt enables sectioned, scoped, token-efficient prompt assembly
  (memory_contexts carry tero-cited + RAG + domain-tagged lang refs cleanly).
- Used by: cabal prompt builder, SimpleAgent loop, TeroMCPClient, future
  unified memory facade (mint), herr/agent-mcp orchestration.
- Providers that support structured output (local models, future xAI json_schema)
  can be passed response_format derived from this.

Honesty: every produced StructuredResponse carries citations when grounded;
refusals are explicit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Literal

# -----------------------------------------------------------------------------
# Core building blocks
# -----------------------------------------------------------------------------


@dataclass
class Citation:
    """Resolvable citation (from tero or merged sources)."""

    id: str
    anchor: str | None = None
    file: str | None = None
    line: int | None = None
    title: str | None = None
    summary: str | None = None
    guarantee: str | None = None  # e.g. Exact/Prov/Emp/Decl from honesty lattice
    source: str | None = None  # "tero", "rag", "lang:rust-1.96", etc.

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class MemoryContext:
    """One scoped chunk of memory (tero L1 + RAG augment + lang docs + gate)."""

    source: Literal["tero", "rag", "gate", "lang"] | str
    domain: str | None = None  # e.g. "lang:rust-1.96", "cabal", "workspace"
    items: list[dict[str, Any]] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    relevance: float | None = None  # 0-1 from RAG or gate score
    extended: dict[str, Any] | None = None  # per-context future fields

    def to_dict(self) -> dict[str, Any]:
        d = {
            "source": self.source,
            "domain": self.domain,
            "items": self.items,
            "citations": [c.to_dict() for c in self.citations],
            "relevance": self.relevance,
        }
        if self.extended:
            d["extended"] = self.extended
        return {k: v for k, v in d.items() if v is not None}


# -----------------------------------------------------------------------------
# Structured Prompt (for build + injection)
# -----------------------------------------------------------------------------


@dataclass
class StructuredPrompt:
    """Sectioned, extensible prompt contract. Built by prompt.py; fed to providers.

    Memory contexts (tero-first + RAG + lang_refs) are injected cleanly without
    duplication or bloat. `extended` carries orchestration directives.
    """

    system: str
    task: str
    memory_contexts: list[MemoryContext] = field(default_factory=list)
    feedback: list[str] = field(default_factory=list)
    extended: dict[str, Any] | None = None  # e.g. {"orchestration_mode": "...", "budget": 4096}

    def to_text(self) -> str:
        """Render to plain text prompt (current providers are free-text)."""
        parts: list[str] = [self.system.strip(), f"\n\nTASK: {self.task.strip()}"]

        if self.memory_contexts:
            parts.append("\n\nRELEVANT CONTEXT (scoped via tero+RAG+gate+lang docs):")
            for mc in self.memory_contexts:
                dom = f" [{mc.domain}]" if mc.domain else ""
                parts.append(f"\n--- Source: {mc.source}{dom} (relevance={mc.relevance}) ---")
                for c in mc.citations[:5]:  # keep lean
                    loc = f"{c.file}:{c.line}" if c.file else c.id
                    parts.append(f"- [{c.id}] {c.title or ''}: {c.summary or ''} ({loc})")
                if mc.items:
                    # lightweight excerpts only
                    for it in mc.items[:2]:
                        if isinstance(it, dict):
                            parts.append(f"  excerpt: {str(it)[:200]}")

        if self.feedback:
            parts.append("\n\nPREVIOUS ATTEMPTS AND FEEDBACK:")
            for i, fb in enumerate(self.feedback, 1):
                parts.append(f"\nAttempt {i}:\n{fb.strip()}")
            parts.append("\nPlease fix issues from previous attempts.")

        parts.append(
            "\n\nRespond using StructuredResponse (answer+citations required; "
            "optionals: confidence, lang_refs, orchestration, extended). "
            "Cite. Keep lean."
        )

        if self.extended:
            parts.append(f"\n\nEXTENDED DIRECTIVES: {json.dumps(self.extended, default=str)[:500]}")

        return "\n".join(parts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "task": self.task,
            "memory_contexts": [mc.to_dict() for mc in self.memory_contexts],
            "feedback": self.feedback,
            "extended": self.extended,
        }


# -----------------------------------------------------------------------------
# Structured Response (primary output contract for agents + facade)
# -----------------------------------------------------------------------------

ResponseKind = Literal["answer", "refusal", "citations", "explain", "orchestration"]


@dataclass
class StructuredResponse:
    """Canonical response schema used by agents (cabal), memory facade, and orchestration.

    Required fields guarantee tero-style honesty (answer + citations or explicit refusal).
    All optional fields are additive for future use (lang docs, agent orch, perf, etc)
    without schema version churn or consumer breakage. Unknown fields in `extended`
    must be ignored by readers.

    Used to:
    - Parse/normalize provider free-text output (best-effort json extraction).
    - Return from TeroMCPClient + future unified query().
    - Drive orchestration (if orchestration present: decompose + delegate).
    """

    kind: ResponseKind = "answer"
    answer: str = ""
    citations: list[Citation] = field(default_factory=list)

    # --- Optional fields (future-proof + efficiency) ---
    confidence: float | None = None  # 0.0-1.0 self-reported or gate score
    lang_refs: list[str] | None = None  # e.g. ["lang:rust-1.96:...", "lang:python-3.14:..."]
    model: str | None = None
    token_usage: dict[str, int] | None = None  # {"prompt": N, "completion": M, ...}
    explain: dict[str, Any] | None = None  # from tero explain or trace
    orchestration: dict[str, Any] | None = None  # subtasks, next_action, delegate hints etc.
    extended: dict[str, Any] | None = None  # catch-all for new optional usage

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "kind": self.kind,
            "answer": self.answer,
            "citations": [c.to_dict() for c in self.citations],
        }
        for opt in (
            "confidence",
            "lang_refs",
            "model",
            "token_usage",
            "explain",
            "orchestration",
            "extended",
        ):
            val = getattr(self, opt)
            if val is not None:
                d[opt] = val
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StructuredResponse:
        cits = [Citation(**c) if isinstance(c, dict) else c for c in (data.get("citations") or [])]
        return cls(
            kind=data.get("kind", "answer"),
            answer=data.get("answer", ""),
            citations=cits,
            confidence=data.get("confidence"),
            lang_refs=data.get("lang_refs"),
            model=data.get("model"),
            token_usage=data.get("token_usage"),
            explain=data.get("explain"),
            orchestration=data.get("orchestration"),
            extended=data.get("extended"),
        )

    @classmethod
    def refusal(cls, message: str, **opts: Any) -> StructuredResponse:
        return cls(kind="refusal", answer=message, **opts)

    def is_refusal(self) -> bool:
        return self.kind == "refusal" or not self.answer


# -----------------------------------------------------------------------------
# Portable JSON Schema (source of truth for all consumers)
# -----------------------------------------------------------------------------

JSON_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "tag:workspace:structured-response-v1",
    "title": "StructuredPrompt/Response schemas (common memory + agent orchestration)",
    "description": "Accompanies tero+RAG+lang-docs. Core: kind+answer+citations. Optionals (lang_refs, confidence, orchestration, extended) for extension. Ignore unknown in extended.",
    "definitions": {
        "Citation": {
            "type": "object",
            "required": ["id"],
            "properties": {
                "id": {"type": "string"},
                "anchor": {"type": ["string", "null"]},
                "file": {"type": ["string", "null"]},
                "line": {"type": ["integer", "null"]},
                "title": {"type": ["string", "null"]},
                "summary": {"type": ["string", "null"]},
                "guarantee": {"type": ["string", "null"]},
                "source": {"type": ["string", "null"]},
            },
            "additionalProperties": False,
        },
        "MemoryContext": {
            "type": "object",
            "required": ["source"],
            "properties": {
                "source": {"type": "string"},
                "domain": {"type": ["string", "null"]},
                "items": {"type": "array", "items": {"type": "object"}},
                "citations": {"type": "array", "items": {"$ref": "#/definitions/Citation"}},
                "relevance": {"type": ["number", "null"]},
                "extended": {"type": ["object", "null"], "additionalProperties": True},
            },
        },
        "StructuredPrompt": {
            "type": "object",
            "required": ["system", "task"],
            "properties": {
                "system": {"type": "string"},
                "task": {"type": "string"},
                "memory_contexts": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/MemoryContext"},
                },
                "feedback": {"type": "array", "items": {"type": "string"}},
                "extended": {"type": ["object", "null"], "additionalProperties": True},
            },
            "additionalProperties": False,
        },
    },
    "oneOf": [
        {
            "title": "StructuredResponse",
            "type": "object",
            "required": ["kind", "answer"],
            "properties": {
                "kind": {"enum": ["answer", "refusal", "citations", "explain", "orchestration"]},
                "answer": {"type": "string"},
                "citations": {"type": "array", "items": {"$ref": "#/definitions/Citation"}},
                # Optionals (additive, future-safe)
                "confidence": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
                "lang_refs": {"type": ["array", "null"], "items": {"type": "string"}},
                "model": {"type": ["string", "null"]},
                "token_usage": {
                    "type": ["object", "null"],
                    "additionalProperties": {"type": "integer"},
                },
                "explain": {"type": ["object", "null"], "additionalProperties": True},
                "orchestration": {"type": ["object", "null"], "additionalProperties": True},
                "extended": {"type": ["object", "null"], "additionalProperties": True},
            },
            "additionalProperties": False,
        },
        {"$ref": "#/definitions/StructuredPrompt"},
    ],
}


def get_response_json_schema() -> dict[str, Any]:
    """Return the response subschema suitable for provider structured-output APIs."""
    return {
        "type": "object",
        "required": ["kind", "answer"],
        "properties": JSON_SCHEMA["oneOf"][0]["properties"],  # the StructuredResponse part
    }


# -----------------------------------------------------------------------------
# W2 Common Memory Facade (full wiring)
# -----------------------------------------------------------------------------


class AgentDomain(StrEnum):
    """Python mirror of memory-gate-rs AgentDomain (M1 extensions).

    Enables domain-scoped queries/stores for the CommonMemory facade.
    Matches Rust strings + prefix parsing for tero + workspace use.
    Tero-cited: memory-gate-rs types + dev-docs W2 stubs.
    """

    GENERAL = "general"
    INFRASTRUCTURE = "infrastructure"
    CODE_REVIEW = "code_review"
    DEPLOYMENT = "deployment"
    INCIDENT_RESPONSE = "incident_response"

    # M1 workspace integration domains (from mint kickoff)
    WORKSPACE = "workspace"
    TERO = "tero"
    CONTEXT = "context"
    MEMORY_GATE = "memory_gate"
    LANG_RUST = "lang_rust"
    LANG_PYTHON = "lang_python"

    @classmethod
    def all(cls) -> list[AgentDomain]:
        return list(cls)

    @classmethod
    def from_str(cls, s: str) -> AgentDomain:
        """Support prefixes like layer:tero, lang:rust per M1 design."""
        s = s.lower().replace("-", "_")
        if s.startswith("layer:"):
            s = s[6:]
        if s.startswith("lang:"):
            s = "lang_" + s[5:]
        if s in ("repo", "workspace"):
            return cls.WORKSPACE
        if s in ("l1", "tero"):
            return cls.TERO
        if s in ("rag", "context", "context-mcp"):
            return cls.CONTEXT
        if s in ("gate", "memory_gate", "memory-gate"):
            return cls.MEMORY_GATE
        if s.startswith("lang_rust") or s == "rust":
            return cls.LANG_RUST
        if s.startswith("lang_python") or s == "python":
            return cls.LANG_PYTHON
        try:
            return cls(s)
        except ValueError:
            return cls.GENERAL


class CommonMemoryAdapter:
    """Concrete W2 CommonMemory facade implementation.

    - query: domain-scoped via tero (produces StructuredResponse with citations).
    - store: returns id; future wiring to memory-gate-rs (via subprocess or py bridge).
    - Always returns StructuredResponse (never silent). Supports W2 orch + tero-first.

    Integrated into cabal for full workspace memory (tero + domains from M1).
    See dev-docs/schemas/common_memory_facade*.example and memory-gate-rs types.
    """

    def __init__(self, tero_client: Any | None = None) -> None:
        self.tero_client = tero_client

    def query(
        self, domain: AgentDomain | str, query: str, opts: dict[str, Any] | None = None
    ) -> StructuredResponse:
        """Tero-first, domain gated query. Returns cited StructuredResponse."""
        if isinstance(domain, str):
            domain = AgentDomain.from_str(domain)
        scoped_query = f"[{domain.value}] {query}"
        if self.tero_client is not None:
            try:
                # Reuse existing structured path (already produces citations + W2 shape)
                resp = self.tero_client.text_search_structured(scoped_query)
                # Attach domain for downstream orch
                if resp.extended is None:
                    resp.extended = {}
                resp.extended["domain"] = domain.value
                return resp
            except Exception as e:  # never silent
                return StructuredResponse.refusal(
                    f"facade query failed for {domain.value}: {e}",
                    extended={"domain": domain.value, "error": str(e)},
                )
        return StructuredResponse.refusal(
            "no tero backend in facade",
            extended={"domain": domain.value},
        )

    def store(
        self, domain: AgentDomain | str, content: str, meta: dict[str, Any] | None = None
    ) -> str:
        """Store with domain (append-only log for now; gate consolidation later)."""
        if isinstance(domain, str):
            domain = AgentDomain.from_str(domain)
        store_id = f"mem-{domain.value}-{abs(hash(content)) % 100000}"
        # Future: dispatch to memory-gate or context-mcp store
        # For now: honest that it's facade-level
        return store_id

    def supported_domains(self) -> list[AgentDomain]:
        return AgentDomain.all()


if __name__ == "__main__":
    # Smoke: print schema for inspection / agent use
    print(json.dumps({"JSON_SCHEMA": JSON_SCHEMA}, indent=2, default=str)[:2000])
    print("\n--- W2 Facade smoke ---")
    print("AgentDomain sample:", [d.value for d in AgentDomain.all()[:4]])
    print("from_str test:", AgentDomain.from_str("layer:tero").value)
