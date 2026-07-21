# Open issues backlog (from intent / gap analysis)

> **1.0.0 SoT (2026-07-21):** [V1_0_0_GAP_ANALYSIS.md](V1_0_0_GAP_ANALYSIS.md) · [V1_0_0_JOINT_EXECUTION.md](V1_0_0_JOINT_EXECUTION.md) · [TOOLING_STACK_READINESS.md](TOOLING_STACK_READINESS.md)  
> Milestone: https://github.com/tzervas/cabal-devmelopner/milestone/1 · Epics #19–#27

Derived from [INTENT_AND_GAP_ANALYSIS.md](INTENT_AND_GAP_ANALYSIS.md). Execution order, waves, and PR DAG: **[ROADMAP.md](ROADMAP.md)**. Use this file as a checklist for GitHub issues or PoC close-out PRs. Update when work lands on `dev`.

Legend: **P0** blocks basic UX · **P1** PoC exit · **P2** MVP foundation · **P3** later

GitHub issues filed from this backlog (2026-07-08): [#2](https://github.com/tzervas/cabal-devmelopner/issues/2)–[#8](https://github.com/tzervas/cabal-devmelopner/issues/8).

---

## P0 — Fix before claiming a working TUI

| ID | GH | Title | Description | Acceptance |
|----|-----|--------|-------------|------------|
| **POC-1** | [#2](https://github.com/tzervas/cabal-devmelopner/issues/2) | TUI console entrypoint broken | `cabal-devmelopner-tui` imports missing `main` | `uv run cabal-devmelopner-tui` launches app; `python -m cabal_devmelopner.tui.app` works |
| **POC-2** | — | Keep Tero enablement docs honest | CLI `--use-tero`, TUI `USE_TERO` (partially fixed in README) | README / PHASE / TERO.md stay aligned after any flag changes |
| **POC-3** | [#3](https://github.com/tzervas/cabal-devmelopner/issues/3) | TUI uses duck-typed Task | `type("Task", …)` instead of dataclass | TUI constructs `Task` from `core.types` |

---

## P1 — PoC exit criteria

| ID | GH | Title | Description | Acceptance |
|----|-----|--------|-------------|------------|
| **POC-4** | [#4](https://github.com/tzervas/cabal-devmelopner/issues/4) | Tero errors silent in agent | `except Exception: pass` around Tero search | Emit progress/error event or log when Tero fails; optional hard-fail flag |
| **POC-5** | — | One-shot MCP only | No session / initialize / tool discovery | Documented limitation **or** proper MCP client session |
| **POC-6** | [#5](https://github.com/tzervas/cabal-devmelopner/issues/5) | Multi-iteration dead code | Always return after iteration 1 | Real feedback path **or** document single-shot and revise PHASE checkbox text |
| **POC-7** | [#6](https://github.com/tzervas/cabal-devmelopner/issues/6) | Thin test suite | Two smoke tests | Cover EventBus, prompt builder, Tero client error paths (mocked), CLI help without API |
| **POC-8** | — | ERROR events on provider failure | TUI handler exists; agent rarely emits | Failures emit `EventType.ERROR` |
| **POC-9** | — | Tero zero-config story | Requires sibling `tero-mcp` + index | Clear setup error messages when paths missing; optional CI skip marker |

---

## P2 — Toward a useful development agent / MVP

| ID | GH | Title | Description | Acceptance |
|----|-----|--------|-------------|------------|
| **MVP-1** | [#8](https://github.com/tzervas/cabal-devmelopner/issues/8) | Minimal tool use | Read file, list dir, run tests | Tool loop + TOOL_CALL / TOOL_RESULT events (started chore/mvp1-tools-start: host+loop+tests; see appended status) |
| **MVP-2** | — | Config system | Model, iterations, Tero paths, workspace | Documented precedence (file / env / flags) |
| **MVP-3** | — | Runtime dependencies | `dependencies = []` | Core + optional extras correct for install story |
| **MVP-4** | [#7](https://github.com/tzervas/cabal-devmelopner/issues/7) | CI: pytest | Only gitleaks today | `uv run pytest` on PR to `dev`/`main` |
| **MVP-5** | — | Streaming | Blocking completions only | Progressive CLI/TUI output |
| **MVP-6** | — | Session / history | Fully isolated runs | Persist or export transcripts (JSONL first; context-mcp optional as **session KV**, not RAG) |
| **MVP-7** | — | Do not treat context-mcp as RAG until legitimate | Pseudo-embeddings + sled/LRU only today; **efficient real RAG is a required upstream goal** | Cabal docs/UI never claim RAG; track upstream embedder+vector+eval; see [LOCAL_TOOLING.md](LOCAL_TOOLING.md) |

---

## P3 — Production-oriented (track only)

| ID | Title |
|----|--------|
| **PROD-1** | Multi-provider (Claude, etc.) |
| **PROD-2** | Discord control + notifications |
| **PROD-3** | Agent swarm / wave execution |
| **PROD-4** | Security-wrapped tools |
| **PROD-5** | Resource management |
| **PROD-6** | True RAG / embeddings — prefer **context-mcp efficient legitimate RAG** (once shipped) and/or Tero L2; never pseudo-embed path |

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

## MVP-1 minimal tools started (chore/mvp1-tools-start appended 2026-07-09)
- Per plan.md p2 (cabal-poc-mvp): B1 tool host v0 (read/list/run + TOOL_* via EventBus) + B2 loop (model propose/execute/re-prompt) + tero/W2 integrate.
- Landed minimal: core/tools.py impl + parse, agent wiring (opt-in --use-tools), cli flag+handlers, prompt tool instr, basic tests (parse/host/agent-loop).
- Still MVP start: no config, limited safety/allow, single tool per turn, no B4 verify yet (iteration remains single-shot until B2+B4).
- Tero-first (script "MVP-1|tool|read_file" + MCP), append-only, branch from main, hygiene + update-tero post.
- Marks MVP-1 in progress (see ROADMAP Wave B, PHASE MVP).
- Cross-cites: plan.md cabal section, roadmap--wave-b..., phase--mvp..., agents (this), wsfull-wave-2026-07-09-compact.md.
- Tero cite expected post update-tero: openissues--mvp-1... + chore/mvp1...

## Status alignment post W2/C0 + PR#12 (appended 2026-07-09, chore/honest-docs-post-w2)
- POC-1 (TUI entrypoint) + POC-3 (real Task): addressed by A1/A2 in PR#12 cab/a1-a3 (now `cabal-devmelopner-tui` has main(); TUI imports/uses core.types.Task).
- POC-4 (Tero errors silent): addressed by C0 fix + A3 (agent now emits EventType.ERROR "CommonMemory facade error..." on facade refusal or except; test_tero_error_emits_event asserts). Facade keeps W2 "always StructuredResponse" (incl refusal); agent owns observability.
- POC-8 (provider ERROR): covered in test_provider_error_emits_and_refusal + agent emit.
- POC-7 (tests): expanded (now covers EventBus, Task, tero+provider error paths; 6 tests green post PR#12).
- POC-2/5/9 remain open (Tero docs honesty, one-shot MCP, zero-config). POC-6 documented as single-shot (see new status alignment below; defer full iter/feedback to MVP per plan.md).
- Conservative: P0/P1 lists above left as backlog reference; resolved items noted here. Cross-cite wsfull-wave-2026-07-09-compact.md §Swarm + PR#12, WORKSPACE_CABAL_TERO_READINESS.md, AGENTS.md (post-c0-fix + review-merge).
- Tero-first (text_search W2/C0/POC + query hits), append-only, no code edits. Update-tero/checks after. See ROADMAP Wave A for execution history.

## POC-6 documented as single-shot (chore/poc6-iteration-honesty appended)
- Per plan.md (cabal section priority 2, "cabal-poc-mvp POC-6"): decide/document as single-shot (honest, defer full feedback to MVP/tools). Matches agent.py reality (if iteration == 1: return).
- Updated status alignment note; POC-6 no longer "remain open" for implementation in P1 (documented limitation).
- Acceptance for POC-6 now: "Real feedback path or document single-shot and revise PHASE checkbox text" — met via documentation.
- Cross-cites: plan.md §1 ("Start with POC-6 decision: document single-shot (honest)..."), PHASE.md, ROADMAP.md (A6 now noted), INTENT_AND_GAP_ANALYSIS.md, wsfull-wave-2026-07-09-compact.md, WORKSPACE_CABAL_TERO_READINESS.md.
- Tero-first via /root/git/scripts/tero.sh + tero MCP (identify, text_search "POC" hits prior, refusals pre-docs on "POC-6|iteration"). Will verify hits post update-tero.
- Append-only targeted; branch chore/poc6-iteration-honesty from main; no src changes. Follow AGENTS dev-workflow/guards.
- Tero cite: will surface openissues--p1-poc... + this section after update-tero.sh cabal-devmelopner.

## MVP-1 complete (chore/cabal-poc-mvp-close appended 2026-07-09)
- Per plan.md priority 2 (cabal-poc-mvp): B1 tool host + B2 loop implemented/verified.
- core/tools.py: ToolHost (read_file/list_dir/run_command allowlisted/safe, confined to workspace_root, timeout, events TOOL_CALL/RESULT emitted), parse_tool_call (regex for "call tool X with k is v"), get_tool_descriptions, execute dispatch.
- agent.py: tools_enabled + tool_host in __init__; in run_structured after provider.complete: parse, if within _max_tool_steps=4 execute + feedback append + continue (re-prompt); else final.
- cli.py: --use-tools flag, TOOL event subs for visibility, pass to SimpleAgent(tools_enabled=..., workspace_root=".")
- prompt.py: injects get_tool_descriptions() into system for StructuredPrompt (integrates with W2/tero path).
- tests/test_smoke.py: test_parse_tool_call_basic, test_tool_host_read_list_local, test_tool_host_run_allowlisted_and_blocks, test_agent_tools_loop_emits_and_reprompts (10/10 green).
- Verified: uv run python -c (parse/host exec OK), pytest full smoke (.......... [100%]).
- Docs/AGENTS/ROADMAP/PHASE/OPEN updated append-only + tero; cross-cites plan.md §1, wsfull-wave..., prior mvp1-start.
- Still limited (MVP start): single tool/turn, no write, config later (B3), full verify/iter (B4 defers POC-6 full). No overclaim.
- Tero-first (script + mcp pre/post), hygiene (check.sh ruff/pytest), branch-guard, append-only.
- Status: MVP-1 done (functional start per acceptance in OPEN). Next B3+ in later waves.
- Tero cite expected: openissues--mvp-1-complete + this section post update-tero.

