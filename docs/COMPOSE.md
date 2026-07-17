# Compose — cabal-devmelopner in the fleet

How this product plugs into **tz-forge**, **agent-harness**, **tg-agent-relay**,
and optional **tero-mcp**. Compose **by reference** — do not vendor full
binaries into every consumer repo.

## Product role

| Field | Value |
|-------|-------|
| GitHub | https://github.com/tzervas/cabal-devmelopner |
| Role | Long-running **dev agent** (CLI / TUI), config-as-code profiles, tero-first AGENTS |
| Status | **Alpha 0.1.x** — usable scaffold; tools MVP-1; not full multi-agent production |
| Default branch | often **`dev`** (check remote HEAD) |
| License | MIT |

## tz-forge: `agent-swarm` kind

[tz-forge](https://github.com/tzervas/tz-forge) project kind **`agent-swarm`**
with assistant profile **`fractal-swarm`** installs a **cabal-profile** module
that points here (compose doc only — no binary embed).

```bash
# from a tz-forge checkout
python3 cli/tz_new.py agent-swarm my-wave --assistant=fractal-swarm
# installs: agents-md-fractal + model-policy + kickoffs + cabal-profile COMPOSE pointer
```

| Module (tz-forge) | What it installs |
|-------------------|------------------|
| `modules/agents/cabal-profile` | `docs/compose/cabal-devmelopner.md` pointer |
| `modules/agents/agents-md-fractal` | Fractal AGENTS (tero-first, L0/L1) |
| `modules/agents/harness-min` | agent-harness compose pointer |
| `modules/agents/model-policy` | L0 frontier / L1 composer policy |

Mirror module doc: `tz-forge/docs/compose/cabal-devmelopner.md`.

## agent-harness

| Field | Value |
|-------|-------|
| Repo | https://github.com/tzervas/agent-harness |
| Role | Universal multi-agent **harness** (orchestrator + swarm dry-run) |
| Boundary | Harness **orchestrates**; cabal is a **leaf executor** / operator CLI |

**Compose rules**

1. Harness owns wave spawn / doctor / dry-run — not cabal.
2. Cabal owns per-repo coding agent loop (providers, tools, Tero client).
3. Prefer docs links + package pins over copy-paste.
4. Offline CI: harness dry-run and cabal `pytest` must not require paid network.

```bash
# sibling layout (optional)
../agent-harness/   # uv run agent-harness doctor
../cabal-devmelopner/
```

## tg-agent-relay

| Field | Value |
|-------|-------|
| Repo | https://github.com/tzervas/tg-agent-relay |
| Role | Telegram / provider / MCP **runtime** bridge |
| Boundary | Relay stays the phone ↔ agent product surface |

**In scope for cabal consumers**

- Future notify hooks via documented relay interfaces
- Shared fleet process (Refs on `dev`, Closes on `main`, no Copilot auto-review)

**Out of scope**

- Vendoring relay into cabal
- Shipping Telegram runtime inside this repo

## tero-mcp (optional sibling)

| Field | Value |
|-------|-------|
| Repo | https://github.com/tzervas/tero-mcp |
| Role | Layer-1 knowledge MCP (`tero-mcp-lite`) |
| Default | **Off** unless `--use-tero` / profile `use_tero` / `USE_TERO=true` |

```text
<git-parent>/
  cabal-devmelopner/
  tero-mcp/                 # optional
  mycelium/                 # optional index source — NEVER auto-cloned by cabal
```

Cabal **does not** automate mycelium install/update. See [TERO.md](TERO.md).

## Config-as-code profiles

| Profile | Model class | Typical use |
|---------|-------------|-------------|
| **l1** | Composer / fast implementer | Default implementation leaves |
| **l0** | Frontier (e.g. grok-4.5) | Hard architecture only |

Example: [cabal.example.toml](../cabal.example.toml). Loader: `core/config.py`.

## 5-minute consumer path

```bash
git clone https://github.com/tzervas/cabal-devmelopner.git
cd cabal-devmelopner
./setup.sh
uv run cabal-devmelopner --version
# Offline smoke (no model call):
uv run pytest -q
./scripts/check.sh --quick
```

Full model run needs **local Ollama** (default) or `XAI_API_KEY`.

## Non-goals

- Embedding cabal binary into tz-forge templates
- Automating mycelium paths
- Replacing agent-harness or tg-agent-relay
- Claiming full multi-agent production readiness before tools + verify + security waves land
