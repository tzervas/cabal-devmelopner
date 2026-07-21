# Release checklist — v1.0.0

## Pre-tag (must be true)

### Product P0 (from V1_0_0_GAP_ANALYSIS)

| ID | Item | Done |
|----|------|------|
| E1.1 | write_file / apply_patch confined | ☐ |
| E1.2 | Tool protocol (structured or golden ≥95%) | ☐ |
| E1.3 | Multi-tool steps | ☐ |
| E2.* | verify_command loop + events | ☑ PR #29 |
| E3.1 | budgets from cabal.toml | ☑ PR #29 |
| E4.1 | Streaming complete | ☐ |
| E5.1 | Tero missing → actionable error | ☐ |
| E5.3 | Session JSONL under `.cabal/runs/` | ☐ |
| E5.4 | No false RAG claims | ☑ docs |
| E6.1 | TUI live log / task / error (minimum dogfood) | ☐ |
| E8.1 | Path confinement property tests | ☐ this PR |
| E8.2 | Security review checklist filled | ☐ |
| E8.4 | Tag + release notes | ☐ |

### Honesty bar

- [ ] README / PHASE / OPEN_ISSUES do **not** claim multi-agent swarm production or legitimate RAG via context-mcp
- [ ] context-mcp Embedder Wave 1 (if linked) is labeled **not RAG until vector store + eval**

### Gates

```bash
./scripts/check.sh --quick
uv run cabal-devmelopner --version
# optional: smoke with local ollama if available
```

### Versioning

1. Bump `VERSION` → `1.0.0`
2. `pyproject.toml` version → `1.0.0`
3. CHANGELOG: move `[Unreleased]` → `[1.0.0] — YYYY-MM-DD`
4. PR to `dev`, then curated land to `main` with `Closes` as needed
5. `git tag v1.0.0 && git push origin v1.0.0`
6. GitHub Release with compose matrix pointer ([COMPOSE.md](COMPOSE.md))

## Compose matrix (1.0)

| Sibling | Min role | Notes |
|---------|----------|-------|
| cabal-devmelopner | leaf agent | this release |
| tero-mcp / tero-rs | optional L1 cites | memory tools need `--features memory` |
| context-mcp | optional session | **not** RAG until Wave 2+ |
| tg-agent-relay | optional notify | E7.1 |
| gha-runner-ctl | CI fleet | self-hosted only |

## Post-tag

- [ ] Update fleet prefer-list warm to include this tag branch if needed
- [ ] Append joint plan exit note
