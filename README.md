# cabal-devmelopner

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage.

## Features (PoC)

- Uses Grok via the raw xAI API
- Tero-MCP integration for codebase-aware context (enabled by default)
- Event-driven architecture (easy to extend with new interfaces)
- Basic iterative agent loop with feedback support
- CLI + functional TUI

## Installation (Development)

```bash
cd cabal-devmelopner
pip install -e .
```

For TUI support:

```bash
pip install -e ".[tui]"
```

## Usage

```bash
export XAI_API_KEY="your-xai-key"

# CLI
cabal-devmelopner "Improve the public API of the compiler frontend"   # Tero context enabled by default

# TUI
cabal-devmelopner-tui
```

Tero-MCP context is **enabled by default**. Use `USE_TERO=false` to disable it.

## Architecture Notes

- **EventBus**: Central communication mechanism (producer/consumer model)
- **Providers**: Pluggable model backends (xAI implemented)
- **MCP Clients**: Tero-MCP client stub available
- Designed to support future features like agent swarms, Discord control, and security-wrapped tools

## Development Phases

See `PHASE.md` for the current roadmap (PoC → MVP → Production).

## License

MIT