# cabal-devmelopner

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage.

## Features (PoC)

- Uses Grok via the raw xAI API
- Optional **Tero-MCP** integration for cited corpus context (docs, decisions, issues)
- Event-driven architecture (easy to extend with new interfaces)
- Basic iterative agent loop with feedback support
- CLI + functional TUI

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

# TUI (recommended way)
uv run cabal-devmelopner-tui

# TUI with Tero
USE_TERO=true uv run cabal-devmelopner-tui

# Or directly with the module
uv run python -m cabal_devmelopner.tui.app
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
| [docs/TERO.md](docs/TERO.md) | Tero-MCP setup, env, Grok tools, agent client |
| [AGENTS.md](AGENTS.md) | Short agent-session notes for Tero lookups |
| [PHASE.md](PHASE.md) | PoC → MVP → Production roadmap |

## Development Phases

See `PHASE.md` for the current roadmap (PoC → MVP → Production).

## License

MIT
