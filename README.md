# cabal-devmelopner

<!-- FLEET-BADGES:BEGIN -->
[![CI](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-ci.yml?query=branch%3Adev)
[![Security](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml/badge.svg?branch=dev)](https://github.com/tzervas/cabal-devmelopner/actions/workflows/fleet-security.yml?query=branch%3Adev)
<!-- FLEET-BADGES:END -->

**cabal-devmelopner** is a **repo-agnostic leaf development agent**: CLI + TUI,
pluggable providers (local Ollama default, xAI optional), optional **Tero-MCP**
cited corpus context, workspace-confined tools (read/list/write/patch/allowlisted
run), post-edit **verify loop**, and per-run **JSONL session** transcripts.

| | |
|--|--|
| **Who** | Operators and L0/L1 agents using cabal as a **leaf** executor |
| **What** | Event-driven agent with config-as-code profiles (`cabal.toml`) |
| **Why** | Trustworthy single-agent co-dev: act → verify → remember (session), without silent RAG claims |

**Status: v0.2.0** (usable leaf). **Not** a multi-agent production platform.
**Not** legitimate RAG (context-mcp is session/embedder Wave 1 only).  
1.0.0 bar: [docs/V1_0_0_GAP_ANALYSIS.md](docs/V1_0_0_GAP_ANALYSIS.md).

## 5-minute path

```bash
git clone https://github.com/tzervas/cabal-devmelopner.git
cd cabal-devmelopner
./setup.sh

uv run cabal-devmelopner --version
# expected: cabal-devmelopner 0.2.0

uv run pytest -q
./scripts/check.sh --quick
```

### Run a task

```bash
# Local model (Ollama on localhost:11434)
uv run cabal-devmelopner "Summarize the project structure"

# Tools + verify (from cabal.toml / defaults)
uv run cabal-devmelopner "Add a docstring to README" --use-tools --use-verify

# Config profiles
cp cabal.example.toml cabal.toml
uv run cabal-devmelopner "Improve error handling" --profile l1

# Frontier
export XAI_API_KEY=...
uv run cabal-devmelopner "Architecture review" --profile l0 --provider xai

# TUI
uv run cabal-devmelopner-tui
```

Sessions write to `.cabal/runs/<task_id>.jsonl` under the workspace.

### Optional: Tero sibling

```text
<git-parent>/
  cabal-devmelopner/
  tero-mcp/          # optional
  tero-rs/           # optional full binary (+ --features memory)
```

```bash
export TERO_TOKENS='local-dev:refresh'
uv run cabal-devmelopner "Query corpus context" --use-tero
```

Guide: [docs/TERO.md](docs/TERO.md). Cabal never auto-installs mycelium.

## Config-as-code

| File | Purpose |
|------|---------|
| [cabal.example.toml](cabal.example.toml) | L0/L1 profiles, tools allowlist, verify_command |
| `cabal.toml` | Local overrides (optional) |

Precedence: **CLI > env > cabal.toml > defaults**.

| Profile | Role | Typical model |
|---------|------|---------------|
| **l1** (default) | Composer | local-ollama `qwen2.5-coder:7b` |
| **l0** | Frontier design | xAI `grok-4.5` |

## Features (0.2.0)

- Local Ollama **and** xAI providers; optional streaming (`--stream`)
- Tools: `read_file`, `list_dir`, `write_file`, `apply_patch`, allowlisted `run_command`
- JSON + free-text tool-call protocol
- Verify loop after tools final answer
- Session JSONL transcripts
- TUI with live tool/verify/error log
- Optional Tero L1 (cited; never silent failures)

> **Not yet (track to 1.0):** Telegram notify (E7), wall-clock budgets (E3.2),
> cancel-in-TUI (E6.2), multi-agent swarm, production security-MCP wrap,
> legitimate RAG (upstream context-mcp Wave 2+).

## Compose stack

See [docs/COMPOSE.md](docs/COMPOSE.md) and [docs/TOOLING_STACK_READINESS.md](docs/TOOLING_STACK_READINESS.md).

| Sibling | Role |
|---------|------|
| tero-mcp / tero-rs | L1 cites (+ optional memory tools) |
| memory-gate-rs | Dense store behind tero-rs `memory` feature |
| context-mcp | Session / Embedder Wave 1 — **not RAG** |
| tg-agent-relay | Notify (E7.1 target) |
| gha-runner-ctl | Self-hosted CI fleet |
| agent-harness | Orchestrator dry-run / wave |

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/V1_0_0_GAP_ANALYSIS.md](docs/V1_0_0_GAP_ANALYSIS.md) | 1.0 bar + epics |
| [docs/V1_0_0_JOINT_EXECUTION.md](docs/V1_0_0_JOINT_EXECUTION.md) | Grok/Claude lanes |
| [docs/RELEASE_1_0_0.md](docs/RELEASE_1_0_0.md) | Pre-tag checklist |
| [docs/SECURITY_REVIEW_1_0.md](docs/SECURITY_REVIEW_1_0.md) | Security checklist |
| [docs/TERO.md](docs/TERO.md) | Tero setup |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [AGENTS.md](AGENTS.md) | Fractal agent rules |

## Development

```bash
./scripts/check.sh --quick
uv run pytest -q
```

Branch model: feature → **`dev`** (`Refs #n`) → **`main`** (`Closes #n`).

## License

MIT — see [LICENSE](LICENSE).

## Release

- Semver: [VERSION](VERSION) / [pyproject.toml](pyproject.toml) / `__version__`
- Current: **v0.2.0** · Target full bar: **v1.0.0** (see gap analysis)
