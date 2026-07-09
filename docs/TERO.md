# Tero-MCP integration

[Tero](https://github.com/tzervas) is a **Layer-1 corpus index** query surface: cited lookups over docs, decisions, issues, changelog entries, and skills. `cabal-devmelopner` talks to **`tero-mcp-lite`** (Python MCP server) over stdio JSON-RPC 2.0.

This document covers local setup, environment variables, Grok/MCP usage, and how the agent client uses Tero. For agent-session quick reference, see [`AGENTS.md`](../AGENTS.md). Upstream server details live in the sibling repo `tero-mcp` (`README.md`, `GENERATING-AN-INDEX.md`).

---

## What Tero is (and is not)

| Is | Is not |
|----|--------|
| A thin MCP front over a pre-built `index.json` | An index *builder* |
| Five query kinds + cite / explain / identify / refresh | Layer-2 / VSA semantic memory |
| Answers with **resolvable citations** (file, line, anchor) | A substitute for reading source docs |
| Typed **refusal** when nothing is citable (never a silent empty hit) | An anonymous/open server (auth required) |

Treat results as **pointers**: open the cited path and read the source. Do not treat summaries as ground truth.

---

## Expected sibling layout

Defaults assume a shared parent directory (e.g. `~/git` or `/root/git`):

```text
<git-parent>/
  cabal-devmelopner/     # this repo
  tero-mcp/              # tero-mcp-lite package
  mycelium/              # corpus + docs/tero-index/index.json
```

Override any of these with environment variables (see below). Paths are resolved from the package location, not the process cwd, so CLI/TUI work from any working directory as long as the sibling checkouts exist.

---

## Prerequisites

1. **Python ≥ 3.11** for `tero-mcp-lite` (this project targets 3.14 via `uv`).
2. **[`uv`](https://docs.astral.sh/uv/)** on `PATH`.
3. Clone and sync **tero-mcp**:

   ```bash
   # from the parent of cabal-devmelopner
   git clone <tero-mcp-url> tero-mcp   # if not already present
   cd tero-mcp && uv sync
   ```

4. A **Tero-shaped** `index.json`. For Mycelium-related work the committed index is:

   ```text
   <git-parent>/mycelium/docs/tero-index/index.json
   ```

   To build an index for another repo, follow `tero-mcp/GENERATING-AN-INDEX.md`.

5. **Tokens.** The server refuses to start without `TERO_TOKENS`. Local/dev placeholder:

   ```bash
   export TERO_TOKENS='local-dev:refresh'
   ```

   Grammar: whitespace/comma-separated `token:scope` pairs (`read` or `refresh`; `refresh` implies `read`). Rotate anything beyond local use; do not commit real secrets.

---

## Environment variables

| Variable | Role | Default (when unset) |
|----------|------|----------------------|
| `TERO_MCP_PROJECT` | Path to the `tero-mcp` uv project | `<git-parent>/tero-mcp` |
| `TERO_INDEX_PATH` | Path to `index.json` | `<git-parent>/mycelium/docs/tero-index/index.json` |
| `TERO_TOKENS` | Server auth table (`token:scope` list) | `{TERO_TOKEN}:refresh` → `local-dev:refresh` |
| `TERO_TOKEN` | Per-call bearer passed as tool arg `token` | `local-dev` |
| `USE_TERO` | TUI only: enable Tero when `true` | `false` |
| `XAI_API_KEY` | xAI API key for the agent (unrelated to Tero auth) | — |

---

## Using Tero from cabal-devmelopner

### CLI (opt-in flag)

```bash
export XAI_API_KEY="your-xai-key"
# optional overrides:
# export TERO_MCP_PROJECT=/path/to/tero-mcp
# export TERO_INDEX_PATH=/path/to/index.json
# export TERO_TOKENS='local-dev:refresh'

uv run cabal-devmelopner "Improve error handling in the compiler frontend" --use-tero
```

Without `--use-tero`, the agent runs with no Tero context.

### TUI (opt-in env)

```bash
export XAI_API_KEY="your-xai-key"
export USE_TERO=true
uv run cabal-devmelopner-tui
```

### What the agent does with results

On each iteration (when a client is configured), `SimpleAgent`:

1. Calls `TeroMCPClient.text_search(task.description, limit=5)`.
2. Formats up to three hits as `id`, title, summary, `file:line`.
3. Injects that block into the prompt via `extra_context`.

Failures are swallowed in PoC so a down or misconfigured server does not abort the task.

### Client API (in-process)

```python
from cabal_devmelopner.mcp.tero_client import TeroMCPClient

client = TeroMCPClient()
client.identify()
client.text_search("transparent memory substrate", limit=5)
client.query_by_id("DN-87")
client.call_tool("query_by_kind", {"value": "rfc"})
```

`TeroMCPClient` launches one `tero-mcp-lite` process per call (stdio, one-shot). It always attaches the bearer `token` and unwraps the MCP `content[].text` JSON envelope into the Tero answer/refusal payload (`kind`, `items`, …).

---

## Using Tero from Grok (MCP)

There are **two** ways work hits Tero:

| Path | When |
|------|------|
| **Grok session MCP** (`tero__*` tools) | Interactive Grok/Build sessions with the server registered |
| **In-repo agent client** (`TeroMCPClient`) | `cabal-devmelopner --use-tero` / `USE_TERO=true` |

They share the same `tero-mcp-lite` binary and index, but registration is independent. A working CLI `--use-tero` does **not** automatically expose `tero__*` tools in Grok, and vice versa.

### Cold start: session has no `tero` server yet

Use this when `search_tool` finds no `tero__*` tools, `grok mcp list` omits `tero`, or a new machine/session never registered the server.

**1. Prerequisites on disk** (one-time)

```bash
# Install uv if needed: https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

# Shared parent (example: ~/git or /root/git)
export GIT_PARENT="${GIT_PARENT:-$HOME/git}"
mkdir -p "$GIT_PARENT"
cd "$GIT_PARENT"

# Clone tero-mcp if missing (use your real remote)
# git clone <tero-mcp-url> tero-mcp
cd tero-mcp && uv sync && cd ..

# Index: Mycelium-shaped example (or generate per tero-mcp/GENERATING-AN-INDEX.md)
# Expect: $GIT_PARENT/mycelium/docs/tero-index/index.json
test -f "$GIT_PARENT/mycelium/docs/tero-index/index.json" \
  || { echo "Missing index.json — set TERO_INDEX_PATH or build an index"; exit 1; }
```

**2. Register the MCP server with Grok** (user scope → `~/.grok/config.toml`)

```bash
export GIT_PARENT="${GIT_PARENT:-$HOME/git}"
export TERO_INDEX="$GIT_PARENT/mycelium/docs/tero-index/index.json"
export TERO_PROJECT="$GIT_PARENT/tero-mcp"

grok mcp add tero \
  -e "TERO_TOKENS=local-dev:refresh" \
  -e "TERO_INDEX_PATH=$TERO_INDEX" \
  -- uv run --project "$TERO_PROJECT" tero-mcp-lite \
       --index "$TERO_INDEX"
```

Project-scoped alternative (commit-friendly; keep secrets as env refs):

```bash
cd /path/to/cabal-devmelopner   # or any project root
grok mcp add tero --scope project \
  -e "TERO_TOKENS=local-dev:refresh" \
  -e "TERO_INDEX_PATH=$TERO_INDEX" \
  -- uv run --project "$TERO_PROJECT" tero-mcp-lite \
       --index "$TERO_INDEX"
```

**3. Equivalent `~/.grok/config.toml` block** (if you prefer editing by hand)

```toml
[mcp_servers.tero]
command = "uv"
args = [
  "run", "--project", "/path/to/tero-mcp",
  "tero-mcp-lite",
  "--index", "/path/to/mycelium/docs/tero-index/index.json",
]
enabled = true

[mcp_servers.tero.env]
TERO_TOKENS = "local-dev:refresh"
TERO_INDEX_PATH = "/path/to/mycelium/docs/tero-index/index.json"
```

Replace `/path/to/...` with absolute paths on your machine (e.g. `/root/git/...` or `$HOME/git/...`).

**4. Verify outside any chat session**

```bash
grok mcp list
grok mcp doctor tero   # expect: command found, handshake OK, 9 tools
```

**5. Make tools visible in the session**

MCP config is loaded when the session starts. After `grok mcp add` or editing `config.toml`:

| Situation | What to do |
|-----------|------------|
| **Server never registered** | Register (step 2), then **start a new Grok session** so tools attach at launch |
| **Config changed mid-session** | In the TUI: `/mcps` → press **`r`** (refresh). If tools still missing, exit and relaunch |
| **Server disabled** | `/mcps` → select `tero` → Space to enable, or set `enabled = true` in config |
| **Doctor fails** | Fix paths/tokens (table below), re-run `grok mcp doctor tero`, then refresh/relaunch |

Do **not** expect `tero__*` tools to appear mid-session without refresh or relaunch after a cold install.

**6. First tool call checklist**

```text
search_tool query="tero identify"
use_tool tero__identify  { "token": "local-dev" }
```

Every Tero tool requires `"token"` matching an entry in `TERO_TOKENS` (local default: `local-dev`).

### Already registered (warm path)

If `grok mcp doctor tero` is healthy but a given session still lacks tools: `/mcps` → **`r`**, or start a new session. Tool names are always namespaced: `tero__text_search`, `tero__query_by_id`, etc. Discover schemas with `search_tool`, then call via `use_tool`.

### Tools (all require `token`)

| Tool | Arguments (plus `token`) | Purpose |
|------|--------------------------|---------|
| `identify` | — | Server name, version, index path, Layer-2 flag |
| `text_search` | `value` | Ranked free-text over id / title / summary |
| `query_by_id` | `value` | Exact id (`RFC-…`, `DN-…`, `M-…`, issue ids) |
| `query_by_kind` | `value` | `rfc`, `adr`, `note`, `issue`, `section`, … |
| `query_by_status` | `value` | `Accepted`, `todo`, `done`, … |
| `cross_ref` | `start`, optional `depth` | BFS on `depends_on` / `doc_refs` |
| `cite` | `kind` + query fields | Citations only |
| `explain` | `kind` + query fields | EXPLAIN trace only |
| `refresh` | — | Reload index from disk (`refresh` scope) |

Grok tool names are namespaced: `tero__text_search`, `tero__query_by_id`, etc. Discover schemas with `search_tool`, then call via `use_tool`.

Example payloads:

```json
{ "value": "transparent memory substrate", "token": "local-dev" }
```

```json
{ "value": "DN-87", "token": "local-dev" }
```

---

## Manual smoke test (no Grok)

```bash
cd /path/to/tero-mcp
export TERO_TOKENS='local-dev:refresh'

echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"identify","arguments":{"token":"local-dev"}}}' \
  | uv run tero-mcp-lite --index /path/to/mycelium/docs/tero-index/index.json
```

Or via this package:

```bash
cd /path/to/cabal-devmelopner
uv run python -c "
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
c = TeroMCPClient()
print(c.identify().get('name'), c.identify().get('version'))
r = c.text_search('DN-87', limit=3)
print(r.get('kind'), len(r.get('items') or []))
"
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Server exits 78 / “no tokens” | `TERO_TOKENS` unset | Export `TERO_TOKENS='local-dev:refresh'` (and set the same in MCP `env`) |
| Exit 66 / load error | Bad or missing `index.json` | Set `TERO_INDEX_PATH` / `--index` to a real index |
| `uv` / project not found | `tero-mcp` not cloned or wrong path | `uv sync` in tero-mcp; fix `--project` path |
| Auth error on `tools/call` | Token not in table or missing arg | Pass `"token": "local-dev"`; match `TERO_TOKENS` |
| **Session never had `tero__*` tools** | Server not registered at launch | Follow [cold start](#cold-start-session-has-no-tero-server-yet); **new session** after `grok mcp add` |
| Grok mid-session missing tools | Config changed / not refreshed | `grok mcp doctor tero`; `/mcps` → `r` or relaunch |
| `doctor` handshake fails | Bad command, env, or index | Fix paths; run the smoke test below outside Grok |
| Empty / refusal `kind` | No citable match | Broaden query; try `query_by_id` / `query_by_kind` |
| Stale index after doc edits | Index not regenerated | Rebuild index, then `refresh` (or restart server) |

---

## Status (PoC)

- [x] `TeroMCPClient` one-shot stdio client with token + envelope unwrap
- [x] Agent injects `text_search` hits into the prompt when enabled
- [x] CLI `--use-tero` and TUI `USE_TERO=true`
- [ ] Long-lived MCP session (shared process, tool discovery framework)
- [ ] Configurable index per-repo without sibling layout assumptions
- [ ] Layer-2 / embeddings / RAG (Production roadmap — see `PHASE.md`)

Upstream package: sibling **`tero-mcp`** (`tero-mcp-lite`). Full Rust stack: Mycelium `mycelium-tero` / `tero-mcp` binary (DN-87).
