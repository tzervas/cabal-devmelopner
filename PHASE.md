# cabal-devmelopner — Development Phases

This document tracks the phased development of `cabal-devmelopner`.

---

## PoC Phase (Current)

**Goal**: Validate core architecture and get a working, extensible agent.

### Deliverables
- [x] Project skeleton + installable CLI
- [x] Event/communication system (producer/consumer model)
- [x] xAI provider (raw API)
- [x] Improved agent loop with iteration + feedback
- [x] Basic prompt construction
- [x] Tero-MCP client integration (basic usage in agent) — see [docs/TERO.md](docs/TERO.md)
- [x] Minimal TUI foundation
- [x] Basic documentation and usage examples ([docs/TERO.md](docs/TERO.md), [AGENTS.md](AGENTS.md), README)
- [ ] PoC testing and stabilization

**Exit Criteria**:
- Can run `cabal-devmelopner "some task"` and get useful output from Grok.
- Architecture is clean and extensible.
- Tero-MCP can be called from the agent (`--use-tero` / `USE_TERO=true`).

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

**Exit Criteria**:
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

**Exit Criteria**:
- Can reliably run long development sessions with minimal human intervention.
- Supports complex workflows involving multiple coordinated agents.
- Security and resource protections are load-bearing.

---

## Notes

- All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture.
- Security and resource management concerns should be considered from MVP onward, even if full implementation lands in Production.
