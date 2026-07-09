# cabal-devmelopner

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage. Status is intentionally conservative: see the [intent and gap analysis](docs/INTENT_AND_GAP_ANALYSIS.md).

## Features (PoC)

- Uses Grok via the raw xAI API
- Optional **Tero-MCP** integration for cited corpus context (docs, decisions, issues) — requires sibling setup
- Event-driven architecture (easy to extend with new interfaces)
- Agent loop scaffold (today: single-shot generation; multi-iteration not yet real)
- CLI works; TUI code exists (**entrypoint currently broken** — tracked as POC-1)

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

Full setup (env vars, Grok MCP registration, tools, troubleshooting): **[docs/TERO.md](docs/TERO.md)**.

## Running

```bash
export XAI_API_KEY="your-xai-key"

# CLI
uv run cabal-devmelopner "Improve the public API of the compiler frontend"

# CLI with Tero context
uv run cabal-devmelopner "Improve the public API of the compiler frontend" --use-tero

# TUI (intended entrypoint — currently fails until POC-1 lands)
uv run cabal-devmelopner-tui

# TUI with Tero (once entrypoint is fixed)
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
| [docs/INTENT_AND_GAP_ANALYSIS.md](docs/INTENT_AND_GAP_ANALYSIS.md) | Product intent vs current reality |
| [docs/OPEN_ISSUES.md](docs/OPEN_ISSUES.md) | P0–P3 backlog from the analysis |
| [docs/TERO.md](docs/TERO.md) | Tero-MCP setup, env, Grok tools, agent client |
| [AGENTS.md](AGENTS.md) | Short agent-session notes for Tero lookups |
| [PHASE.md](PHASE.md) | PoC → MVP → Production roadmap (honest checkboxes) |

## Development Phases

See [PHASE.md](PHASE.md) for the roadmap. PoC is **not exited** until P0 TUI entrypoint and basic stabilization items are addressed.

## License

MIT
