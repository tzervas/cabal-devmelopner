# Intent and Gap Analysis

**Baseline:** `dev` (includes Tero docs/client commit `32d30d3`)  
**Analysis date:** 2026-07-08  
**Status:** Living document — update when PoC exit criteria or architecture change.

This document records product **intent**, **current implementation reality**, and the **gaps** between them. Prefer this file over marketing phrasing in the README when they disagree. Trackable work items: [OPEN_ISSUES.md](OPEN_ISSUES.md). Related setup: [TERO.md](TERO.md), [PHASE.md](../PHASE.md).

---

## 1. Stated intent

| Layer | Intent |
|--------|--------|
| **Product** | A **repo-agnostic development agent** for long-running, high-quality coding assistance |
| **PoC (current)** | Validate architecture: installable CLI, event bus, xAI provider, iterative agent, basic Tero-MCP, minimal TUI |
| **MVP** | Daily co-dev tool: full TUI, solid context/config, notifications, verification loop, long-lived process |
| **Production** | Multi-agent swarms, multi-provider, Discord control, security/resource management, true RAG |

**Core principles:** repo-agnostic · extensible communications · strong Tero integration · clean architecture.

---

## 2. Current implementation (snapshot)

Approximate application size: ~550+ LOC under `src/cabal_devmelopner/`.

| Area | Status | Notes |
|------|--------|--------|
| Project skeleton + CLI | **Present** | `cabal-devmelopner` works with `XAI_API_KEY` |
| EventBus | **Present** | Sync subscribe/emit; used by CLI + TUI |
| xAI provider | **Present** | Raw HTTPS to `/v1/responses`; heuristic response parsing |
| Prompt builder | **Minimal** | Task + optional context + feedback strings |
| Agent loop | **Scaffold** | Multi-iteration structure exists; **always returns after iteration 1** |
| Tero-MCP client | **PoC client** | Sibling-layout defaults (`../tero-mcp`, Mycelium index); one-shot stdio; token + envelope parse |
| Tero usage in agent | **Wired (opt-in)** | CLI `--use-tero` / TUI `USE_TERO=true`; failures swallowed |
| TUI | **Partial / broken entrypoint** | UI code exists; console script `main` missing (`ImportError`) |
| Docs | **Improved** | README, PHASE, `docs/TERO.md`, `AGENTS.md` |
| Tests | **Smoke only** | Two tests; both pass |
| CI | **Partial** | Gitleaks only; no pytest/ruff/mypy gates |
| Setup | **Present** | `setup.sh` + `uv sync --all-extras` |

### Architecture (as implemented)

```text
CLI / TUI  →  SimpleAgent  →  Provider.complete(prompt)
                 │                └─ XaiProvider (HTTP)
                 ├─ EventBus (progress / generation / complete)
                 └─ TeroMCPClient.text_search (opt-in; sibling tero-mcp-lite)
```

There is **no tool-use loop**, no filesystem edits, no shell execution, no verification, and no multi-turn conversation state beyond a one-shot completion.

---

## 3. PoC checklist: intent vs reality

| PoC deliverable | Honest status | Notes |
|-----------------|---------------|--------|
| Project skeleton + CLI | **Done** | |
| Event system | **Done** | Basic; no queue/async/unsubscribe |
| xAI provider | **Done** | Fragile parsing |
| Iterative agent + feedback | **Partial** | Feedback path is effectively dead code |
| Basic prompt construction | **Done** | Thin |
| Tero-MCP client integration | **Partial → usable with siblings** | Client improved; needs external `tero-mcp` + index; still one-shot MCP |
| Minimal TUI foundation | **Partial** | Code present; **entrypoint broken** |
| Docs / usage examples | **Mostly done** | Tero documented; this analysis closes status honesty |
| PoC testing & stabilization | **Open** | Smoke only |

### PoC exit criteria

| Criterion | Met? |
|-----------|------|
| Run `cabal-devmelopner "task"` and get useful Grok output | **Partial** — single-shot chat; no code changes on disk |
| Architecture clean and extensible | **Directional** — seams exist; not proven under real tools |
| Tero-MCP callable from the agent | **Conditional** — yes if sibling layout + tokens configured; not zero-config |

---

## 4. Critical gaps

### 4.1 Not a development agent yet

**Intent:** coding assistance that acts on repositories.  
**Reality:** one-shot LLM completion (+ optional corpus context).

- No tools (read/write files, search, shell, git, tests)
- No apply / diff / edit workflow
- No verification (tests, linters, human review hooks)
- `EventType.TOOL_CALL`, `TOOL_RESULT`, `NEEDS_HUMAN_INPUT` defined but unused

### 4.2 TUI entrypoint broken (P0)

```text
cabal-devmelopner-tui → ImportError: cannot import name 'main'
```

`pyproject.toml` → `cabal_devmelopner.tui.app:main`, but `app.py` has no `main()` and no `__main__` guard. README’s recommended TUI path fails.

### 4.3 Tero: improved but incomplete

**Landed improvements (dev):** sibling defaults, env overrides, token auth, MCP content envelope unwrap, `items`-based agent formatting, `docs/TERO.md`.

**Remaining:**

| Issue | Detail |
|-------|--------|
| External dependency | Requires sibling `tero-mcp` + index (e.g. Mycelium); not vendored |
| Protocol | One process / one `tools/call`; no `initialize` / session / tool discovery |
| Silent failure | Agent `except Exception: pass` hides Tero errors |
| Product scope | Corpus/docs index — not full codebase RAG |
| Docs overclaim risk | PHASE checkbox “done” implies more completeness than out-of-the-box UX |

### 4.4 Agent loop does not iterate

```python
if iteration == 1:
    ...
    return response  # always
```

`max_iterations` and feedback never matter on the success path. Tests document single provider call even when `max_iterations=3`.

### 4.5 Empty runtime dependencies

```toml
dependencies = []
```

Textual is only under optional extra `tui`. Local setup uses `--all-extras`; bare installs may omit TUI.

### 4.6 TUI bypasses `Task` type

Duck-typed `type("Task", (), {...})()` instead of `Task` dataclass.

### 4.7 Status drift (pre this docs update)

PHASE marked TUI and docs fully done while TUI entrypoint failed and multi-iteration remained nominal. Prefer checkboxes that match [OPEN_ISSUES.md](OPEN_ISSUES.md).

---

## 5. Secondary / structural gaps

| Gap | Impact |
|-----|--------|
| No config system | Only env vars / flags |
| No streaming | Blocking full completions |
| Sync EventBus + threads | PoC-OK; not designed thread-safe |
| xAI response parsing | May return raw JSON dumps |
| No session state | No history / resume / queue |
| CI: tests/lint | Only gitleaks |
| Python ≥ 3.14 | Narrow contributor surface |
| ERROR events | Rarely emitted on provider failure |
| Security / resource limits | Not started (later phases) |

---

## 6. What is solid (keep)

- Clear phase model (PoC → MVP → Production)
- Seams: `core` / `providers` / `mcp` / `tui`
- Provider ABC for multi-provider later
- EventBus as extension point (CLI, TUI, future Discord)
- uv-first workflow + `setup.sh`
- Tero documentation and improved client baseline
- Smoke tests + `MockProvider`
- LICENSE, gitleaks, `.gitignore`

---

## 7. Gap map by phase

```text
                    INTENT                          CURRENT STATE
PoC ────────────────────────────────────────────────────────────
  CLI + xAI                                       mostly done
  TUI foundation                                  code yes; entrypoint broken
  Tero-MCP basic                                  client+docs; needs siblings
  Real iteration / feedback                       early-return
  Stabilization / tests                           smoke only

MVP ────────────────────────────────────────────────────────────
  Full TUI, config, notifications                 not started
  Verification loop                               TODO in agent
  Long-lived process / packaging                  not started

Production ─────────────────────────────────────────────────────
  Swarms, multi-provider, Discord, security       not started
```

---

## 8. Recommended priority (close PoC honestly)

1. **POC-1** Fix TUI `main` entrypoint (+ optional `__main__`).
2. **POC-3** TUI constructs real `Task`.
3. **POC-6** Either implement one verification/feedback path or document single-shot and adjust PHASE wording.
4. **POC-4 / POC-5** Surface Tero errors; document failure modes; consider session MCP later.
5. **POC-7** Expand tests (EventBus, prompt, Tero error paths, CLI without live API).
6. **MVP-3 / MVP-4** Runtime deps honesty + pytest CI.
7. **MVP-1** Minimal tools so the product matches “development agent.”

Details: [OPEN_ISSUES.md](OPEN_ISSUES.md).

---

## 9. Bottom line

**Intent:** long-running, repo-agnostic **development agent** with event-driven UIs and strong Tero context.

**Reality:** early **architecture PoC** with a working CLI→xAI path, improved opt-in Tero client/docs, event seams, and an incomplete TUI — **not yet** a development agent (no tools/verification) and **not yet** a polished PoC exit (broken TUI entrypoint, nominal multi-iteration).

**Largest honesty gap:** claiming full TUI / iterative agent completion ahead of behavior.  
**Largest product gap:** no tools or verification, so the system cannot act on a codebase.
