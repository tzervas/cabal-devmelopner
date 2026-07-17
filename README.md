# cabal-devmelopner

<!-- FLEET-BADGES:BEGIN -->
[![CI](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml?query=branch%3Adev)
[![Security](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml?query=branch%3Adev)
<!-- FLEET-BADGES:END -->

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage. Status is intentionally conservative: see the [intent and gap analysis](docs/INTENT_AND_GAP_ANALYSIS.md).

## Features (PoC)

- Uses Grok via the raw xAI API
- Optional **Tero-MCP** integration for cited corpus context (docs, decisions, issues) — requires sibling setup
- Event-driven architecture (easy to extend with new interfaces)
- Agent loop scaffold (today: single-shot generation; multi-iteration not yet real)
- CLI works; TUI code + entrypoint works (POC-1/POC-3 fixed in PR#12 cab/a1-a3); still PoC surface (see docs)

> **Not yet:** file/tools loop, verification, multi-agent, or zero-config Tero.

## Setup (Recommended: UV)

This project uses `uv` for Python version management, dependency resolution, and running.

### One-command setup (Ubuntu / WSL / macOS / Linux)

```bash
git clone https://github.com/tzervas/cabal-devmelopner.git
cd cabal-devmelopner
./setup.sh
```

### Manual setup

```bash
# 1. Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and enter the repo
cd cabal-devmelopner

# 3. Sync environment
uv sync --all-extras
```

### Tero (optional, for corpus context)

Tero is **opt-in**. Defaults expect sibling checkouts next to this repo:

```text
<git-parent>/
  cabal-devmelopner/
  tero-mcp/          # MCP server package
  mycelium/          # provides docs/tero-index/index.json
```

```bash
cd ../tero-mcp && uv sync   # once
export TERO_TOKENS='local-dev:refresh'
```

Full setup (env vars, **cold-start Grok MCP install** when a session lacks `tero`, tools, troubleshooting): **[docs/TERO.md](docs/TERO.md)**.

## Running

```bash
# Local self-hosted (default, GPU on 5080; full pipeline with tero + W2 schemas)
uv run cabal-devmelopner "Refactor using memory-gate + tero" --use-tero --local-model qwen2.5-coder:7b

# Frontier explicit
export XAI_API_KEY=...
uv run cabal-devmelopner "High-level orch review" --provider xai --model grok-4.5 --use-tero

# TUI (entrypoint fixed PR#12 A1; PoC surface)
uv run cabal-devmelopner-tui

# TUI with Tero
USE_TERO=true uv run cabal-devmelopner-tui
```

| Surface | How to enable Tero |
|---------|-------------------|
| CLI | Pass `--use-tero` |
| TUI | Set `USE_TERO=true` |

## Architecture Notes

- **EventBus**: Central communication mechanism (producer/consumer model)
- **Providers**: Pluggable model backends (xAI implemented)
- **MCP Clients**: `TeroMCPClient` — one-shot stdio client for `tero-mcp-lite` (see [docs/TERO.md](docs/TERO.md))
- Designed to support future features like agent swarms, Discord control, and security-wrapped tools

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/ROADMAP.md](docs/ROADMAP.md) | Full product plan: waves, PR DAG, corpus alignment |
| [docs/LOCAL_TOOLING.md](docs/LOCAL_TOOLING.md) | Sibling MCP/tools readiness (incl. context-mcp ≠ RAG) |
| [docs/INTENT_AND_GAP_ANALYSIS.md](docs/INTENT_AND_GAP_ANALYSIS.md) | Product intent vs current reality |
| [docs/OPEN_ISSUES.md](docs/OPEN_ISSUES.md) | P0–P3 backlog from the analysis |
| [docs/TERO.md](docs/TERO.md) | Tero-MCP setup, env, Grok tools, agent client |
| [AGENTS.md](AGENTS.md) | Short agent-session notes for Tero lookups |
| [PHASE.md](PHASE.md) | PoC → MVP → Production roadmap (honest checkboxes) |

## Development Phases

See [PHASE.md](PHASE.md) for the roadmap. PoC is **not exited** until P0 TUI entrypoint and basic stabilization items are addressed.

## License

MIT

## Latest Wave (W2 + Facade, PR process)

W2 CommonMemoryAdapter + AgentDomain (M1) fully wired in core/schemas.py + agent.py (run_structured uses facade for tero domain queries, StructuredResponse + citations). Legacy compat + provider opts.

C0 critical fixed (2026-07-09): facade errors now cause agent to emit EventBus ERROR (never silent) even on explicit refusal return; test updated + passes.

See AGENTS.md for full, dev-docs/waves/wsfull-wave-2026-07-09-compact.md (Tero cite: workspacecabalteroreadiness--wave-2026-07-09-complete-compacted-for-context-optimization), WORKSPACE_CABAL_TERO_READINESS.md.

Part of PR#12. After doc/tero updates + checks, pr-review (adapted rubric: tero-first, W2, C0, M1, guards, hygiene) + merge if clean.

## Post-fix append (C0 resolved) 2026-07-09

- W2 CommonMemory facade (CommonMemoryAdapter + AgentDomain M1 from memory-gate-rs) implemented in core/schemas.py + wired into agent (run_structured uses facade for TERO-domain tero queries + W2 StructuredResponse/Prompt with citations).
- PR #12 (cab/a1-a3-tui-errors-tests) includes facade, A1-A3 (TUI entry/errors/tests), wiring, doc updates (AGENTS/ROADMAP/INTENT/TERO/PHASE/kickoffs/README), tero re-index.
- Integration: cabal + tero (local index auto-discover), hygiene, C0 (honesty gate), M1 domains. See dev-docs/WORKSPACE_CABAL_TERO_READINESS.md + waves/wsfull-wave-2026-07-09-compact.md .
- Kickoffs/agent/claude files updated (tero-first, dev-workflow, guards, facade/W2 refs).
- Tero index + docs updated as part of PR; run update-tero.sh after edits.
- Prefer: local-ollama + --use-tero + W2 structured (full pipeline). Follow tero-first, hygiene, security, branch/worktree guards, dev-workflow (append-only).

Docs + tero always updated in PR process. See AGENTS.md for agent context. Tero cites: readme--latest-wave-w2-facade-pr-process .
