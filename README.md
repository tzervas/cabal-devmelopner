# cabal-devmelopner

**cabal-devmelopner** is a repo-agnostic development agent designed for long-running, high-quality coding assistance.

It is currently in **PoC** stage.

## Features (PoC)

- Uses Grok via the raw xAI API
- Optional Tero-MCP integration for codebase-aware context
- Event-driven architecture (easy to extend with new interfaces)
- Basic iterative agent loop with feedback support
- CLI interface (TUI foundation started)

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

# Basic usage
cabal-devmelopner "Improve the public API of the compiler frontend"

# With Tero context
cabal-devmelopner "Review recent changes to the type checker" --use-tero
```

## Architecture Notes

- **EventBus**: Central communication mechanism (producer/consumer model)
- **Providers**: Pluggable model backends (xAI implemented)
- **MCP Clients**: Tero-MCP client stub available
- Designed to support future features like agent swarms, Discord control, and security-wrapped tools

## Development Phases

See `PHASE.md` for the current roadmap (PoC → MVP → Production).

## License

MIT
