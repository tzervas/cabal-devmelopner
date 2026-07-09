# Intent and Gap Analysis

**Baseline:** `dev` (includes Tero docs/client commit `32d30d3`)  
**Analysis date:** 2026-07-08  
**Status:** Living document — update when PoC exit criteria or architecture change.

This document records product **intent**, **current implementation reality**, and the **gaps** between them. Prefer this file over marketing phrasing in the README when they disagree. Trackable work items: [OPEN_ISSUES.md](OPEN_ISSUES.md). Ordered waves + PR plan: [ROADMAP.md](ROADMAP.md). Related setup: [TERO.md](TERO.md), [PHASE.md](../PHASE.md).

---

## 1. Stated intent

| Layer | Intent |
|--------|--------|
| **Product** | A **repo-agnostic development agent** for long-running, high-quality coding assistance |
| **PoC (current)** | Validate architecture: installable CLI, event bus, xAI provider, iterative agent, basic Tero-MCP, minimal TUI |
| **MVP** | Daily co-dev tool: full TUI, solid context/config, notifications, verification loop, long-lived process |
| **Production** | Multi-agent swarms, multi-provider, Discord control, security/resource management, true RAG |

**Core principles:** repo-agnostic · extensible communications · strong Tero integration · clean architecture.

## Recent Updates (W2 + Facade, as of PR process 2026-07-09)

- W2 schemas + CommonMemory facade implementation landed in core/schemas.py: StructuredResponse/Prompt (W2), Citation, MemoryContext, AgentDomain (M1 mirror from memory-gate-rs: TERO/CONTEXT/MEMORY_GATE/LANG_*/WORKSPACE etc with from_str prefix), CommonMemoryAdapter (query -> StructuredResponse w/ cites, store stub).
- Wiring in agent (core/agent.py): facade now drives TERO mem_contexts + structured resp in run_structured (C0 honesty: errors surfaced via EventBus, never silent).
- Integration via cabal + tero (auto local index), hygiene, C0/M1 (ctx feature/ctx-c0-honesty, mint feature/mint-m1-domain-facade).
- Docs (this, PHASE, ROADMAP, AGENTS, kickoffs/README.md, TERO, README) updated with facade, W2 schemas/StructuredResponse, PR #12, tero, dev-workflow/guards refs.
- Kickoffs, agent context (AGENTS.md), claude files updated to latest (facade/W2, tero-first, guards).
- Tero indexes refreshed post-doc changes (update-tero.sh); included in PR #12.
- PR #12 (cab/a1-a3-tui-errors-tests branch) for review (pr-review skill adapted: tero cites, W2/ facade, C0 gate, M1 domains from memory-gate, dev-workflow, branch/worktree guards, hygiene/security, append-only, tero-first) then merge.
- See wsfull-wave-2026-07-09-compact.md (W2, local models, parameterized skills, leaf reviews), WORKSPACE_CABAL_TERO_READINESS.md (facade + cabal integration, tero readiness, dev branches).

Update docs + tero as part of PRs. Gaps tracked in OPEN_ISSUES. Tero-first.

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
| Tero usage in agent | **Wired (opt-in + W2 facade)** | CLI `--use-tero` / TUI `USE_TERO=true`; facade (CommonMemoryAdapter) primary; failures emit ERROR (C0/POC-4 fixed PR#12) |
| Tero as Grok MCP | **Documented** | Session tools (`tero__*`) require `grok mcp add` + launch/refresh; cold-start install in [TERO.md](TERO.md) |
| TUI | **PoC complete entrypoint (PR#12)** | main() + real Task (A1/A2/POC-1/3); error handlers; full polish later (Wave B) |
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
| Minimal TUI foundation | **Partial (entrypoint landed)** | Code + main() + Task wiring (PR#12 A1-A3); still PoC (no full status etc) |
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

### 4.2 TUI entrypoint (P0 — addressed PR#12)

Entrypoint now present (`def main()` + `__main__` guard in app.py; console script wired). TUI uses real `Task` dataclass (POC-3). Error events wired (A3). 

Still PoC-grade: limited widgets, no full live status polish (Wave B). README TUI path now functional (once XAI etc configured). See A1-A3 in PR#12 + wsfull compact.

### 4.3 Tero: improved but incomplete

**Landed improvements (dev):** sibling defaults, env overrides, token auth, MCP content envelope unwrap, `items`-based agent formatting, `docs/TERO.md`.

**Remaining:**

| Issue | Detail |
|-------|--------|
| External dependency | Requires sibling `tero-mcp` + index (e.g. Mycelium); not vendored |
| Protocol | One process / one `tools/call`; no `initialize` / session / tool discovery |
| Silent failure | Addressed for facade path (C0): agent emits ERROR on is_refusal() + except (see agent.py:80-118); legacy compat note |
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

### 4.7 Status drift (pre updates)

Prior docs lagged post-code (e.g. "broken" after A1-A3 in PR#12). This + parallel edits in PHASE/ROADMAP/OPEN_ISSUES close the honesty gap (chore/honest-docs-post-w2). Prefer matching OPEN_ISSUES + cites to wsfull-wave-2026-07-09-compact.md. Multi-iteration still nominal (see 4.4).

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
  TUI foundation                                  code + entrypoint + Task (PR#12); PoC surface
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

1. **POC-6** (remaining) Document or implement iteration/feedback (still early-return on iter=1); adjust PHASE if needed.
2. **POC-7** (in progress) Expand tests (EventBus/prompt/Tero+provider errs done post PR#12; CI next).
3. **POC-5/9** Tero: one-shot vs session; zero-config messages.
4. **MVP-3 / MVP-4** Runtime deps + pytest CI.
5. **MVP-1** Minimal tools...
(POC-1/3/4/8 addressed in PR#12 A1-A3 + C0; see appended + OPEN_ISSUES status.)

Details: [OPEN_ISSUES.md](OPEN_ISSUES.md).

---

## 9. Bottom line

**Intent:** long-running, repo-agnostic **development agent** with event-driven UIs and strong Tero context.

**Reality:** early **architecture PoC** with working CLI→xAI, W2 CommonMemory facade + tero (AgentDomain), opt-in + Grok MCP Tero, event seams, TUI entrypoint+Task+errors fixed (PR#12 A1-A3/C0) — **not yet** a development agent (no tools/verification) and **not yet** a polished PoC exit (iteration POC-6 nominal, tests/CI partial).

**Largest honesty gap:** claiming full TUI / iterative agent completion ahead of behavior.  
**Largest product gap:** no tools or verification, so the system cannot act on a codebase.

### Appended post-W2 facade + C0 (2026-07-09, PR#12 process)
- W2 CommonMemory facade (schemas + agent wiring for StructuredResponse + domain queries via tero) closes integration gap for workspace memory.
- C0 blocker fixed: tero errors now emit ERROR events (never silent) when using facade path.
- Updated docs, AGENTS, kickoffs, tero index as required. See wsfull-wave compact + readiness for citations and full state.
- Enables PR review/merge, up-merge, propagate. All per dev-workflow, tero-first, append-only.

### Honest status alignment (chore/honest-docs-post-w2, 2026-07-09)
- Fixed lagging text in PoC snapshot/checklist/gaps/priority/bottom-line (TUI entrypoint/POC-1/3, Tero C0/POC-4 now accurate per merged code; iteration kept partial).
- Cross-cites: wsfull-wave-2026-07-09-compact.md (W2 facade, A1-A3, C0 fix, PR#12), WORKSPACE_CABAL_TERO_READINESS.md (post-wave integration), PHASE/ROADMAP/OPEN_ISSUES/AGENTS (appends).
- Tero-first (MCP: text_search "W2 Facade" "C0" "POC" "wsfull-wave"; identify + cited reads of dev-docs) before any edits. Append-only edits. Process followed exactly (main pull, branch chore/honest-docs-post-w2, check.sh, signed commit, gh pr to main).
- Tero cite example: workspacecabalteroreadiness--w2-facade-cabal-integration-post-wsfull-wave-2026-07-09-compact + agents--post-c0-fix-for-pr12-2026-07-09-appended. No code touched. Hygiene via check --quick.
