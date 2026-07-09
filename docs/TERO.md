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

Register the server once (user scope example):

```bash
grok mcp add tero \
  -e TERO_TOKENS=local-dev:refresh \
  -e TERO_INDEX_PATH=/path/to/mycelium/docs/tero-index/index.json \
  -- uv run --project /path/to/tero-mcp tero-mcp-lite \
       --index /path/to/mycelium/docs/tero-index/index.json
```

Or edit `~/.grok/config.toml`:

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

Verify:

```bash
grok mcp doctor tero   # expect: handshake OK, 9 tools
```

If tools are missing mid-session: `/mcps` → **`r`** (refresh), or start a new session.

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
| Server exits 78 / “no tokens” | `TERO_TOKENS` unset | Export `TERO_TOKENS='local-dev:refresh'` |
| Exit 66 / load error | Bad or missing `index.json` | Set `TERO_INDEX_PATH` to a real index |
| `uv` / project not found | `tero-mcp` not cloned or wrong path | Set `TERO_MCP_PROJECT` |
| Auth error on `tools/call` | Token not in table or missing arg | Pass `"token": "local-dev"`; match `TERO_TOKENS` |
| Grok has no `tero__*` tools | MCP not reloaded | `grok mcp doctor tero`; `/mcps` → `r` or new session |
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
