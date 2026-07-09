# Agent notes — cabal-devmelopner

## Tero (documentation / corpus context) — now dynamic over tero-rs

Use **Tero** (Python presenter over tero-rs binary) for cited lookups. The surface (tools, args, inputSchemas with Rust type hints, categories: introspection/query/explain/maintenance) is **dynamically discovered** at runtime via `--describe`. Python renders (loose hints + early schema validation + rich errors); Rust backend ensures strict validation + execution + Layer-2 when gated.

Prefer tero before greps. Full guide: **[docs/TERO.md](docs/TERO.md)**. Categories help smart scoping (e.g. query tools for cross-repo relevant knowledge without bloat).

See workspace vision for common memory (tero + context-mcp + memory-gate-rs), local llama.cpp/GPU, cross-repo scoped reuse, token optimization.

**Kickoff framework**: root `.claude/kickoffs/cab.md` + `wsfull.md` owns the work here. Use fresh `/kickoff cab`. Apply partial mycelium workflow (dev-workflow, tero-first with categories, guards, wave). Local `.claude/kickoffs/README.md`.

### Prefer

1. `text_search` / `query_by_id` / `query_by_kind` via the **tero** MCP server (when registered in Grok).
2. Open the **cited file:line** — treat hits as pointers, not ground truth.
3. On refusal (`kind: refusal` / no citable match), rephrase or fall back to normal repo search.

### Subagents and multi-repo excavation (required when Tero is available)

Sibling-tool investigations, readiness audits, and design waves are **harder** if agents only `ls`/`grep` checkouts. **Every agent that excavates** (orchestrator *and* leaf subagents) should use Tero first for corpus memory, then verify against local trees.

**Orchestrator checklist when spawning investigation agents:**

1. Confirm `tero__identify` (or `search_tool` → `tero__*`) works; if not, follow cold-start below before launching a wave.
2. Put an explicit **Tero excavation block** in every subagent prompt (copy below). Do not assume the child will invent it.
3. Prefer leaf prompts that name **ids to chase** when known (`DN-87`, `M-1017`, RFC/ADR numbers, skill names).
4. After leaves return, orchestrator may `cross_ref` / `query_by_id` on any new ids the leaves surfaced.

**Paste into each investigation subagent prompt:**

```text
## Tero excavation (do this before deep filesystem greps)

You have access to the `tero` MCP server (tools `tero__*`). Use it to excavate project
memory related to your target. Token: "local-dev" (or env TERO_TOKEN).

1. search_tool query="tero" once if needed to refresh schemas.
2. tero__identify { "token": "local-dev" } — confirm index is live.
3. tero__text_search { "value": "<target name + MCP/security/agent keywords>", "token": "local-dev" }
4. For each strong hit with an id (DN-…, M-…, RFC-…, E…): tero__query_by_id
5. tero__cross_ref { "start": "<id>", "depth": "2", "token": "local-dev" } when mapping programs
6. Open cited file:line paths under the mycelium (or other) tree — summaries are not ground truth.
7. Only then dig the local sibling checkout (branches, README, src, tests).

If tero__* tools are missing: note "Tero unavailable" in the report and fall back to repo search;
tell the orchestrator to fix MCP registration for the next wave.
```

**Why:** The Mycelium index holds decisions, issues, and skills that explain *why* a sibling MCP exists and what “done” means. Local clones alone miss paused design intent and cross-repo links.

### If this session has no `tero__*` tools

Sessions only pick up MCP servers registered **before launch** (or after `/mcps` → **`r`**). Quick path:

```bash
# 1) One-time: sibling package + index (adjust GIT_PARENT)
export GIT_PARENT="${GIT_PARENT:-$HOME/git}"
cd "$GIT_PARENT/tero-mcp" && uv sync   # clone tero-mcp first if missing
test -f "$GIT_PARENT/mycelium/docs/tero-index/index.json"

# 2) Register (user scope → ~/.grok/config.toml)
grok mcp add tero \
  -e TERO_TOKENS=local-dev:refresh \
  -e "TERO_INDEX_PATH=$GIT_PARENT/mycelium/docs/tero-index/index.json" \
  -- uv run --project "$GIT_PARENT/tero-mcp" tero-mcp-lite \
       --index "$GIT_PARENT/mycelium/docs/tero-index/index.json"

# 3) Verify, then new session (or /mcps → r if already inside TUI)
grok mcp doctor tero   # handshake OK, 9 tools
```

Details, project scope, config.toml, and troubleshooting: **[docs/TERO.md § Cold start](docs/TERO.md#cold-start-session-has-no-tero-server-yet)**.

### Grok MCP (when available)

- Server name: `tero` → tools namespaced `tero__…`
- Every tool call requires `"token": "local-dev"` (or whatever matches `TERO_TOKENS`)
- Typical index: sibling `mycelium/docs/tero-index/index.json`
- Typical package: sibling `tero-mcp` (`tero-mcp-lite`)
- If tools are missing mid-session: `/mcps` → `r`, or new session; `grok mcp doctor tero`

| Tool | Use for |
|------|---------|
| `text_search` | Free-text (`value`) over id/title/summary |
| `query_by_id` | Exact id (`RFC-…`, `DN-…`, `M-…`) |
| `query_by_kind` | `rfc`, `adr`, `note`, `issue`, `section`, … |
| `query_by_status` | `Accepted`, `todo`, `done`, … |
| `cross_ref` | BFS on depends_on/doc_refs from `start` |
| `cite` / `explain` | Citations-only or EXPLAIN trace |
| `identify` | Server + index identity |
| `refresh` | Reload index from disk (`refresh` scope) |

```text
search_tool query="tero text_search"
use_tool tero__text_search  { "value": "…", "token": "local-dev" }
use_tool tero__query_by_id  { "value": "DN-87", "token": "local-dev" }
```

### This repo’s agent CLI/TUI

Independent of Grok MCP registration:

```bash
export XAI_API_KEY="your-xai-key"   # required for cabal-devmelopner itself
uv run cabal-devmelopner "…" --use-tero
USE_TERO=true uv run cabal-devmelopner-tui
```

Env overrides: `TERO_MCP_PROJECT`, `TERO_INDEX_PATH`, `TERO_TOKENS`, `TERO_TOKEN` (defaults assume `../tero-mcp` and `../mycelium/docs/tero-index/index.json` under the same git parent).
