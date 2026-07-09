# Agent notes — cabal-devmelopner

## Tero (documentation / corpus context)

Use **Tero** for cited lookups over the corpus index before guessing from memory or grepping the whole tree. Full project guide (including **cold-start install** when a session has no server): **[docs/TERO.md](docs/TERO.md)**.

### Prefer

1. `text_search` / `query_by_id` / `query_by_kind` via the **tero** MCP server (when registered in Grok).
2. Open the **cited file:line** — treat hits as pointers, not ground truth.
3. On refusal (`kind: refusal` / no citable match), rephrase or fall back to normal repo search.

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
