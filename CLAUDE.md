# cabal-devmelopner — Claude / coding-assistant context

## Overview

**cabal-devmelopner** is a repo-agnostic development agent (CLI + TUI) with
event-driven architecture, optional Tero-MCP corpus context, and MVP-1 tools.
Status: **alpha (0.1.x)** — honest PoC/MVP scaffolding, not a full production
multi-agent platform.

## Project map

```
src/cabal_devmelopner/
  cli.py              # CLI entry (config-as-code + providers)
  core/
    agent.py          # SimpleAgent + structured / tools loop
    config.py         # cabal.toml loader (L0/L1 profiles)
    events.py         # EventBus
    schemas.py        # W2 StructuredResponse + CommonMemory facade
    tools.py          # ToolHost (read_file / list_dir / run_command)
    prompt.py types.py
  mcp/tero_client.py  # optional Tero one-shot client
  providers/          # xAI + local-ollama
  tui/app.py          # Textual TUI (PoC surface)
tests/                # pytest smoke + config
scripts/check.sh      # local CI gate
cabal.example.toml    # config-as-code template
docs/                 # ROADMAP, TERO, COMPOSE, intent/gap
AGENTS.md             # fractal agent rules (tero-first)
```

## Development commands

```bash
./setup.sh                 # one-shot: uv + sync
./scripts/check.sh         # ruff + mypy(advisory) + pytest
./scripts/check.sh --quick # skip mypy
./scripts/check.sh --fix   # format + lint fix attempt

uv run cabal-devmelopner --version
uv run cabal-devmelopner "smoke task"   # needs local ollama or XAI_API_KEY
uv run pytest -q
```

## Config-as-code

Copy `cabal.example.toml` → `cabal.toml` (optional). Profiles:

| Profile | Role | Default provider hint |
|---------|------|------------------------|
| **l1** | Composer / implementer (default) | local-ollama |
| **l0** | Frontier / hard architecture | xai (grok-4.5) |

Precedence: **CLI flags > env > cabal.toml > defaults**.

Tero is **opt-in** (sibling `tero-mcp` + index). **No mycelium automation.**

## Coding standards

- Prefer small, reviewable diffs
- No secrets in commits or logs
- Run `./scripts/check.sh` before claiming complete
- Do **not** enable automatic Copilot code review on PRs
- Append-only for living docs (`AGENTS.md`, ROADMAP status sections)
- Tero-first when the `tero` MCP server is available (see AGENTS.md)

## PR hygiene

| Target | Keywords |
|--------|----------|
| Feature → `dev` | **`Refs #n`** only |
| Delivery → `main` | **`Closes #n`** / **`Fixes #n`** |

Branch from `dev`. Never push directly to `main`.

## Compose

How this plugs into **tz-forge** `agent-swarm`, **agent-harness**, and
**tg-agent-relay**: [docs/COMPOSE.md](docs/COMPOSE.md).

## Further reading

- [README.md](README.md) — 5-minute path
- [AGENTS.md](AGENTS.md) — fractal L0/L1 + tero excavation
- [docs/TERO.md](docs/TERO.md) — Tero-MCP cold start
- [docs/ROADMAP.md](docs/ROADMAP.md) — waves
- [PHASE.md](PHASE.md) — PoC → MVP honesty
- [docs/FLEET_STANDARDS.md](docs/FLEET_STANDARDS.md) — CI / issue close policy
