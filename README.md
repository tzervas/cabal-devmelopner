# cabal-devmelopner

<!-- FLEET-BADGES:BEGIN -->
[![CI](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml?query=branch%3Adev)
[![Security](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml?query=branch%3Adev)
<!-- FLEET-BADGES:END -->

**cabal-devmelopner** is a **repo-agnostic development agent** for long-running,
high-quality coding assistance: CLI + TUI, pluggable model providers (local
Ollama by default, xAI/Grok optional), optional **Tero-MCP** cited corpus
context, and an MVP tools loop (`read_file` / `list_dir` / `run_command`).

| | |
|--|--|
| **Who** | Operators and fractal L0/L1 agent swarms working in tzervas (or any) repos |
| **What** | Event-driven agent with config-as-code profiles (`cabal.toml`) |
| **Why** | One honest leaf executor that prefers local models + Tero-first memory over silent RAG claims |

**Status: alpha (v0.1.0).** Usable scaffold — not a full multi-agent production
platform. See [PHASE.md](PHASE.md) and [docs/INTENT_AND_GAP_ANALYSIS.md](docs/INTENT_AND_GAP_ANALYSIS.md).

## 5-minute path

```bash
git clone https://github.com/tzervas/cabal-devmelopner.git
cd cabal-devmelopner
./setup.sh

# Offline smoke (no model / no network API required)
uv run cabal-devmelopner --version
# expected: cabal-devmelopner 0.1.0

uv run pytest -q
# expected: all tests passed

./scripts/check.sh --quick
# expected: OK: cabal-devmelopner checks passed
```

### Optional: run a real task

Default provider is **local-ollama** (self-hosted). Frontier needs `XAI_API_KEY`.

```bash
# Local model (Ollama must be up on localhost:11434)
uv run cabal-devmelopner "Summarize the project structure"

# With config profile (copy example first)
cp cabal.example.toml cabal.toml
uv run cabal-devmelopner "Improve error handling" --profile l1

# Frontier explicit
export XAI_API_KEY=...
uv run cabal-devmelopner "High-level architecture review" --profile l0 --provider xai

# TUI
uv run cabal-devmelopner-tui
```

### Optional: Tero sibling (corpus context)

Tero is **opt-in**. Cabal does **not** auto-install mycelium or tero-mcp.

```text
<git-parent>/
  cabal-devmelopner/
  tero-mcp/          # optional MCP server package
  mycelium/          # optional: docs/tero-index/index.json (handoff only)
```

```bash
cd ../tero-mcp && uv sync   # once, if you want Tero
export TERO_TOKENS='local-dev:refresh'
cd ../cabal-devmelopner
uv run cabal-devmelopner "Refactor using memory-gate + tero" --use-tero
```

Full guide: **[docs/TERO.md](docs/TERO.md)**.

## Config-as-code

| File | Purpose |
|------|---------|
| [cabal.example.toml](cabal.example.toml) | Documented template (L0/L1 profiles, tero-first, tools allowlist) |
| `cabal.toml` | Your local overrides (optional; not required for smoke) |

| Profile | Role | Typical model hint |
|---------|------|--------------------|
| **l1** (default) | Composer / implementer | local-ollama `qwen2.5-coder:7b` |
| **l0** | Frontier / hard architecture | xAI `grok-4.5` |

Precedence: **CLI flags > env > cabal.toml > defaults**.

## Features (alpha)

- Grok via raw xAI API **or** local Ollama
- Optional **Tero-MCP** for cited corpus context
- Event-driven architecture (easy to extend)
- MVP-1 tools loop (`--use-tools`)
- CLI + TUI entrypoints
- W2 StructuredResponse + CommonMemory facade (tero domain)

> **Not yet:** full verification loop, multi-agent swarms, zero-config Tero,
> production security wrappers.

## Architecture

- **EventBus** — producer/consumer events
- **Providers** — pluggable backends (`local-ollama`, `xai`)
- **Config** — `core/config.py` + `cabal.toml` profiles
- **MCP** — `TeroMCPClient` one-shot stdio client for `tero-mcp-lite`
- **Compose** — plugs into tz-forge `agent-swarm`, agent-harness, relay ([docs/COMPOSE.md](docs/COMPOSE.md))

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/COMPOSE.md](docs/COMPOSE.md) | tz-forge / harness / relay / tero compose |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Waves, PR DAG, corpus alignment |
| [docs/TERO.md](docs/TERO.md) | Tero-MCP setup, cold start, troubleshooting |
| [docs/LOCAL_CHECKS.md](docs/LOCAL_CHECKS.md) | Local CI parity |
| [docs/FLEET_STANDARDS.md](docs/FLEET_STANDARDS.md) | Fleet CI + issue close policy |
| [AGENTS.md](AGENTS.md) | Fractal agent rules (tero-first) |
| [CLAUDE.md](CLAUDE.md) | Coding-assistant project context |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [PHASE.md](PHASE.md) | PoC → MVP → Production (honest checkboxes) |

## Development

```bash
./scripts/check.sh          # ruff + mypy(advisory) + pytest
./scripts/check.sh --fix
uv run ruff check src tests
uv run pytest -q
```

Branch model: feature → **`dev`** (`Refs #n`) → **`main`** (`Closes #n`).
No automatic Copilot code review.

## License

MIT — see [LICENSE](LICENSE).

## Release

- Semver in [pyproject.toml](pyproject.toml) / [VERSION](VERSION) / package `__version__`
- Notes: [CHANGELOG.md](CHANGELOG.md)
- Tag path: `v0.1.0` (GitHub Release notes for 0.x+)
