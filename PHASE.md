# cabal-devmelopner — Development Phases

This document tracks the phased development of `cabal-devmelopner`.

For honest status vs intent (including known P0/P1 gaps), see **[docs/INTENT_AND_GAP_ANALYSIS.md](docs/INTENT_AND_GAP_ANALYSIS.md)** and the backlog in **[docs/OPEN_ISSUES.md](docs/OPEN_ISSUES.md)**.

**Full product plan (waves + PR DAG):** **[docs/ROADMAP.md](docs/ROADMAP.md)** — maps PoC → MVP → Production onto ordered work, with Tero/corpus alignment.

---

## PoC Phase (Current)

**Goal**: Validate core architecture and get a working, extensible agent.

### Deliverables

- [x] Project skeleton + installable CLI
- [x] Event/communication system (producer/consumer model)
- [x] xAI provider (raw API)
- [~] Improved agent loop with iteration + feedback — *loop scaffold only; always returns after first generation (see POC-6)*

## Recent Wave Updates (W2 Facade + Integration, 2026-07-09)

As part of wsfull PR process:
- W2 CommonMemory facade implementation + AgentDomain M1 (mirror memory-gate-rs): CommonMemoryAdapter + Structured* W2 schemas (Citation/MemoryContext/StructuredResponse etc) in schemas.py.
- Wiring in agent: facade.query(AgentDomain.TERO..) drives memory + structured in run_structured (C0 honesty, error surfacing).
- PR #12 (cab/a1-a3-tui-errors-tests): facade + A1-A3 TUI/errors/tests + wiring + doc updates (AGENTS, README, docs/ROADMAP, INTENT_AND_GAP_ANALYSIS, TERO, PHASE, .claude/kickoffs/README.md) + tero reindex.
- Integration via cabal + tero (local index), hygiene, C0 (honesty gate), M1 domains.
- Kickoffs, agent context (AGENTS.md), claude files updated to latest (facade/W2 refs, tero-first, dev-workflow, branch/worktree guards).
- Docs + tero updated as part of PR process; run update-tero after edits.
- See wsfull-wave-2026-07-09-compact.md (W2, local-ollama+tero+W2 pipeline, parameterized hygiene/security-scan/codegen, leaf C0/M1), WORKSPACE_CABAL_TERO_READINESS.md (facade cabal integration, tero readiness).
- Review via adapted pr-review skill (tero citations, W2 schemas/StructuredResponse, CommonMemory facade, C0 gate, M1, dev-workflow, guards, hygiene/security, append-only, tero-first); merge if +ve.
- Tero-first, dev-workflow, guards followed for changes.

See compact, readiness, PR for details. Update docs + tero before land.
- [x] Basic prompt construction
- [~] Tero-MCP client integration — *opt-in client + docs; requires sibling `tero-mcp` + index (see [docs/TERO.md](docs/TERO.md)); errors still swallowed (POC-4)*
- [~] Minimal TUI foundation — *UI present; console entrypoint broken (`main` missing, POC-1)*
- [x] Basic documentation and usage examples ([README](README.md), [docs/TERO.md](docs/TERO.md), [AGENTS.md](AGENTS.md), intent/gap docs)
- [ ] PoC testing and stabilization (POC-7)

`[x]` done · `[~]` partial / conditional · `[ ]` not done

### Exit Criteria

| Criterion | Status |
|-----------|--------|
| Can run `cabal-devmelopner "some task"` and get useful output from Grok | **Partial** — single-shot completion; no repo edits |
| Architecture is clean and extensible | **Directional** — seams in place |
| Tero-MCP can be called from the agent | **Conditional** — `--use-tero` / `USE_TERO=true` with sibling layout |
| TUI launches via documented entrypoints | **Not met** — fix POC-1 |

**PoC not exited** until P0 entrypoint is fixed and testing/stabilization is honest about remaining partials.

---

## MVP Phase

**Goal**: Make `cabal-devmelopner` a practical daily co-dev tool.

### Key Features

- Full-featured TUI (status, progress, logs, task management)
- Solid context management using Tero-MCP
- Easy configuration system
- Notification channels (Discord webhook + Telegram)
- Improved agent loop with real verification/feedback
- Basic support for running as a long-lived process
- Packaging and easy installation (`uv tool install`)
- Minimal tool use so the agent can act on a codebase (see MVP-1)

### Exit Criteria

- Comfortable to use for real development work.
- Can run for extended periods with decent context handling.
- Notifications work reliably.

---

## Production Phase

**Goal**: Robust, scalable, multi-agent development system.

### Key Features

- Multi-provider support (xAI, Claude, others)
- Full Discord control (task submission, monitoring, approvals)
- Agent swarm orchestration (multiple swarms running simultaneously)
- Wave-based execution patterns ("wave n" style)
- Safe concurrent file modification ("lowest common owner" model)
- Advanced Tero + Context MCP integration (including embeddings + true RAG)
- Resource management (memory, disk, context windows)
- Security layer (hardwired wrapping of tools like webpuppet via Security MCP)
- Persistent state and session management
- High reliability and polish

### Exit Criteria

- Can reliably run long development sessions with minimal human intervention.
- Supports complex workflows involving multiple coordinated agents.
- Security and resource protections are load-bearing.

---

## Notes

- All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture.
- Security and resource management concerns should be considered from MVP onward, even if full implementation lands in Production.
- Prefer updating checkboxes here when code lands; keep narrative detail in the intent/gap analysis.
