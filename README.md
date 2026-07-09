# cabal-devmelopner

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage.

## Features (PoC)

- Uses Grok via the raw xAI API
- Tero-MCP integration for codebase-aware context (enabled by default)
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

## Running

```bash
export XAI_API_KEY="your-xai-key"

# CLI
uv run cabal-devmelopner "Improve the public API of the compiler frontend"

# TUI (recommended way)
uv run cabal-devmelopner-tui

# Or directly with the module
uv run python -m cabal_devmelopner.tui.app
```

Tero-MCP context is **enabled by default**. Set `USE_TERO=false` to disable it.

## Architecture Notes

- **EventBus**: Central communication mechanism (producer/consumer model)
- **Providers**: Pluggable model backends (xAI implemented)
- **MCP Clients**: Tero-MCP client stub available
- Designed to support future features like agent swarms, Discord control, and security-wrapped tools

## Development Phases

See `PHASE.md` for the current roadmap (PoC → MVP → Production).

## License

MIT