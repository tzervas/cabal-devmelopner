#!/usr/bin/env bash
#
# One-command setup for cabal-devmelopner (Ubuntu/WSL/macOS/Linux)
# Usage: ./setup.sh
#

set -e

echo "==> Checking for uv..."
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Installing required Python version (from .python-version)..."
uv python install

echo "==> Syncing project (including dev + TUI extras)..."
uv sync --all-extras

echo ""
echo "✅ Setup complete!"
echo ""
echo "5-minute smoke:"
echo "  uv run cabal-devmelopner --version"
echo "  uv run pytest -q"
echo "  ./scripts/check.sh --quick"
echo ""
echo "Run a task (local Ollama default; or set XAI_API_KEY for xai):"
echo "  uv run cabal-devmelopner \"your task here\""
echo "  uv run cabal-devmelopner-tui"
echo ""
echo "Optional config: cp cabal.example.toml cabal.toml"
echo "Optional Tero sibling: see docs/TERO.md (not auto-installed)"
echo ""
echo "To activate the virtual environment manually:"
echo "  source .venv/bin/activate"
