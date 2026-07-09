# Open issues backlog (from intent / gap analysis)

Derived from [INTENT_AND_GAP_ANALYSIS.md](INTENT_AND_GAP_ANALYSIS.md). Use as a checklist for GitHub issues or PoC close-out PRs. Update when work lands on `dev`.

Legend: **P0** blocks basic UX · **P1** PoC exit · **P2** MVP foundation · **P3** later

---

## P0 — Fix before claiming a working TUI

| ID | Title | Description | Acceptance |
|----|--------|-------------|------------|
| **POC-1** | TUI console entrypoint broken | `cabal-devmelopner-tui` imports missing `main` | `uv run cabal-devmelopner-tui` launches app; `python -m cabal_devmelopner.tui.app` works |
| **POC-2** | Keep Tero enablement docs honest | CLI `--use-tero`, TUI `USE_TERO` (partially fixed in README) | README / PHASE / TERO.md stay aligned after any flag changes |
| **POC-3** | TUI uses duck-typed Task | `type("Task", …)` instead of dataclass | TUI constructs `Task` from `core.types` |

---

## P1 — PoC exit criteria

| ID | Title | Description | Acceptance |
|----|--------|-------------|------------|
| **POC-4** | Tero errors silent in agent | `except Exception: pass` around Tero search | Emit progress/error event or log when Tero fails; optional hard-fail flag |
| **POC-5** | One-shot MCP only | No session / initialize / tool discovery | Documented limitation **or** proper MCP client session |
| **POC-6** | Multi-iteration dead code | Always return after iteration 1 | Real feedback path **or** document single-shot and revise PHASE checkbox text |
| **POC-7** | Thin test suite | Two smoke tests | Cover EventBus, prompt builder, Tero client error paths (mocked), CLI help without API |
| **POC-8** | ERROR events on provider failure | TUI handler exists; agent rarely emits | Failures emit `EventType.ERROR` |
| **POC-9** | Tero zero-config story | Requires sibling `tero-mcp` + index | Clear setup error messages when paths missing; optional CI skip marker |

---

## P2 — Toward a useful development agent / MVP

| ID | Title | Description | Acceptance |
|----|--------|-------------|------------|
| **MVP-1** | Minimal tool use | Read file, list dir, run tests | Tool loop + TOOL_CALL / TOOL_RESULT events |
| **MVP-2** | Config system | Model, iterations, Tero paths, workspace | Documented precedence (file / env / flags) |
| **MVP-3** | Runtime dependencies | `dependencies = []` | Core + optional extras correct for install story |
| **MVP-4** | CI: pytest | Only gitleaks today | `uv run pytest` on PR to `dev`/`main` |
| **MVP-5** | Streaming | Blocking completions only | Progressive CLI/TUI output |
| **MVP-6** | Session / history | Fully isolated runs | Persist or export transcripts |

---

## P3 — Production-oriented (track only)

| ID | Title |
|----|--------|
| **PROD-1** | Multi-provider (Claude, etc.) |
| **PROD-2** | Discord control + notifications |
| **PROD-3** | Agent swarm / wave execution |
| **PROD-4** | Security-wrapped tools |
| **PROD-5** | Resource management |
| **PROD-6** | True RAG / embeddings (beyond Layer-1 index) |

---

## Suggested GitHub issue titles

1. `[P0] Fix cabal-devmelopner-tui entrypoint (missing main)`
2. `[P0] TUI: construct real Task dataclass`
3. `[P1] Surface Tero failures instead of silent pass`
4. `[P1] Document or implement real multi-iteration agent feedback`
5. `[P1] Expand smoke tests beyond SimpleAgent happy path`
6. `[P1] Emit EventType.ERROR on provider/agent failures`
7. `[P2] Add minimal filesystem tools to agent loop`
8. `[P2] CI workflow for pytest on dev/main`

---

## Out of scope for the docs PR that added this file

- Implementing the fixes above
- Changing runtime behavior (except via future code PRs)
