# cabal-devmelopner — Product Roadmap

**Status:** Plan (2026-07-08)  
**Baseline:** `dev` + docs on `docs/intent-gap-analysis` (intent/gap, Tero cold-start)  
**Living with:** [PHASE.md](../PHASE.md) · [INTENT_AND_GAP_ANALYSIS.md](INTENT_AND_GAP_ANALYSIS.md) · [OPEN_ISSUES.md](OPEN_ISSUES.md) · [TERO.md](TERO.md)

This document turns phase goals and the open backlog into **ordered waves**, **dependencies**, and a **PR plan**. It is the implementation plan for “the rest” of the product after the architecture PoC.

---

## 1. North star

**cabal-devmelopner** is a **repo-agnostic development agent**: long-running, event-driven, multi-surface (CLI / TUI / future Discord), with **strong Tero integration** for cited project memory and an extensible tool/provider core.

It is **not** Mycelium’s ADK phylum (RFC-0023 / M-671) and **not** mycelium-tero itself (DN-87 / E39-1). Those are **upstream patterns and APIs** this product **consumes and mirrors in Python**:

| Upstream (Mycelium corpus via Tero) | What cabal borrows |
|-------------------------------------|--------------------|
| **DN-87** Layer-1 index + mandatory citations; Layer-2 VSA later (M-1018) | Context: Tero client, never-silent refusals, no fake RAG claims |
| **M-1015** (done) corpus Layer-1 index | Default sibling index path |
| **M-1017** (todo) MCP + HTTP fronts + skills | Prefer real MCP session when available; cold-start register path |
| **wave** skill / fractal swarm | Production: disjoint worktrees, lowest-common-owner merges |
| **RFC-0023** Agent/Tool/Session/Runner map | Conceptual model for tools, events, multi-agent later |
| **E22-1 / security-review skill** | Production security wrappers; MVP-era hooks only |

**Honesty rule (from DN-87 §6):** Layer-1 answers with citations only; improved-on-RAG stays aspirational until measured. Cabal must not claim “true RAG” before PROD-6.

**Agent excavation rule:** Orchestrators and leaf subagents investigating siblings or designing features **use Tero first** (see [AGENTS.md](../AGENTS.md#subagents-and-multi-repo-excavation-required-when-tero-is-available) and [TERO.md](TERO.md#subagents-must-excavate-with-tero-too)). Inject the checklist into every subagent prompt; do not assume children discover MCP tools on their own.

---

## Semver Releases (appended 2026-07-10)

Per workspace plan + user: semver + GPG releases established across projects (local podman GHCR for any dist images).

- This project baseline: v0.1.0 (no prior tags; matches pyproject).
- See AGENTS.md##Semver for process (uv build, -s tag, gh release, tero update).
- Podman for containers (see peri example; herr-doktor will follow).
- Bumps only with hygiene, docs/tero updates, cites to plan.

Cites: plan.md, Tero version/release searches, git baselines.

## 2. Current position (summary)

| Area | State |
|------|--------|
| CLI + xAI one-shot | Works |
| EventBus + Provider ABC | Seams ready |
| Tero client + docs + Grok cold-start | Usable with siblings; opt-in |
| TUI | Code present + entrypoint works (A1/POC-1 + POC-3 fixed PR#12); PoC surface |
| Agent loop | Single-shot; multi-iteration dead (POC-6) |
| Tools / verify / multi-agent | Not started |

**PoC exit** requires honest tests/stabilization (POC-7); iteration (POC-6) now documented single-shot (honest, per plan.md p2 deferral to MVP/tools); TUI launch (POC-1) + Tero error surfacing (POC-4) addressed in PR#12 (A1-A3). **MVP exit** requires tools + verification + usable TUI/config. **Production** is multi-agent + security + resources. Cross-cite wsfull-wave-2026-07-09-compact.md + plan.md.

Filed issues today: GitHub **#2–#8** (see OPEN_ISSUES).

---

## 3. Architecture target (incremental)

```text
                    ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
 Surfaces           │ CLI         │  │ TUI         │  │ Discord/…    │
                    └──────┬──────┘  └──────┬──────┘  └──────┬───────┘
                           │                │                 │
                           └────────────────┼─────────────────┘
                                            ▼
                                    ┌───────────────┐
                                    │   EventBus    │  (async-ready later)
                                    └───────┬───────┘
                                            ▼
                                    ┌───────────────┐
                                    │ Agent Runner  │  loop + budgets + tools
                                    └───────┬───────┘
                          ┌─────────────────┼─────────────────┐
                          ▼                 ▼                 ▼
                   ┌────────────┐   ┌────────────┐   ┌────────────────┐
                   │ Providers  │   │ Tool host  │   │ Context (Tero) │
                   │ xAI, …     │   │ fs/shell/  │   │ L1 now; L2 later│
                   └────────────┘   │ git/test   │   └────────────────┘
                                    └────────────┘
```

**Principles**

1. **Event-first surfaces** — all UIs subscribe; agent never prints only to stdout for “real” work.
2. **Tools are first-class** — `TOOL_CALL` / `TOOL_RESULT` events (types already exist).
3. **Tero is optional but first-class** — same enablement contract as today; failures never silent after Wave A.
4. **Repo-agnostic** — workspace root is config; no hard-coded product paths except Tero sibling defaults.
5. **Security and budgets early as hooks** — full enforcement in Production; interfaces appear in MVP.

---

## 4. Waves

### Wave A — PoC close-out (make claims true)

**Goal:** Documented entrypoints work; status docs match code; minimal regression net.

| ID | Work | GH | Depends |
|----|------|-----|---------|
| A1 | TUI `main` + `__main__` | #2 POC-1 | — |
| A2 | TUI uses `Task` dataclass | #3 POC-3 | A1 optional parallel |
| A3 | Surface Tero failures (events/log) | #4 POC-4 | — |
| A4 | ERROR events on provider failure | POC-8 | — |
| A5 | Expand smoke tests | #6 POC-7 | A1–A4 preferred |
| A6 | Multi-iteration honesty | #5 POC-6 | documented single-shot (plan.md p2; defer to MVP/tools) |
| A7 | pytest CI workflow | #7 MVP-4 | A5 |
| A8 | Runtime deps honesty (`textual` extra) | MVP-3 | — |

\* **A6 (POC-6):** documented as single-shot per plan.md (cabal-poc-mvp priority 2) + decision in chore/poc6-iteration-honesty. Keep PHASE `[~]` for iteration (scaffold only); full feedback/verify loop deferred until tools + Wave B (B2/B4). See wsfull-wave-2026-07-09-compact.md.

**Exit:** `uv run cabal-devmelopner-tui` works (A1 landed PR#12); `pytest` green in CI (A5 partial); PHASE PoC partials only for intentional deferrals (e.g. POC-6). A1/A2/A3 + C0 facade error path completed in PR#12 (cab/a1-a3-tui-errors-tests). See wsfull-wave-2026-07-09-compact.md.

---

### Wave B — Minimum useful agent (MVP core)

**Goal:** Agent can **act on a repo** with Tero-assisted context and a real loop.

| ID | Work | Notes |
|----|------|--------|
| B1 | **Tool host v0** | `read_file`, `list_dir`, `run_command` (allowlisted) or `run_tests`; emit TOOL_* events |
| B2 | **Tool-using agent loop** | Model proposes tools → execute → re-prompt; max steps budget |
| B3 | **Workspace / config** | `cabal.toml` or `.cabal-devmelopner.toml`: model, max_steps, tero on/off, workspace root, allowlist |
| B4 | **Verification hook** | After tools: run tests/lint command from config; feed failures as feedback (closes real POC-6) |
| B5 | **Tero session client (optional)** | Long-lived MCP or documented one-shot; clear errors if index missing (POC-5/POC-9) |
| B6 | **TUI v1** | Status, log stream, task input, cancel; fix threading vs EventBus |
| B7 | **Streaming** | Provider stream → PROGRESS/partial events → TUI/CLI |
| B8 | **Session transcript** | Append JSONL per run under `.cabal/` or user config path |
| B9 | **context-mcp (optional)** | Session store sidecar only — **not RAG** (see [LOCAL_TOOLING.md](LOCAL_TOOLING.md#context-mcp-not-legitimate-rag-yet--and-must-become-efficient-legitimate-rag)) |

**context-mcp product need:** **efficient legitimate RAG is required** on that project (real embedder + vector retrieval + eval) — not optional polish. Today: hash pseudo-embeddings + LRU/`sled` KV only. Cabal uses it as session memory until that exit criteria lands; PROD-6 may then consume it as RAG (or Tero L2). Details: [LOCAL_TOOLING.md](LOCAL_TOOLING.md).

**Exit:** One developer can point cabal at a repo, enable Tero, run a task that reads files and runs tests, and see a useful result without hand-copying model output.

**Maps to PHASE MVP:** tools, verification, config, long-lived-ish TUI, packaging prep.

## MVP-1 tools start (chore/mvp1-tools-start, 2026-07-09 appended)
- B1: core/tools.py (ToolHost + read_file/list_dir/run_command allowlisted + parse + events TOOL_CALL/RESULT).
- B2: wired in agent.py (tools_enabled flag, loop detect/parse/execute/feedback re-prompt limited _max_tool_steps; compat non-tool path preserved).
- CLI: --use-tools flag + event subs + pass to SimpleAgent.
- Prompt: tool format + get_tool_descriptions injected (integrates tero/W2 Structured in same path).
- Tests: parse, host fs/run safety, agent tool loop (mock propose+final).
- Docs updated append-only (this, OPEN_ISSUES, PHASE, AGENTS).
- Tero-first (script + mcp), branch chore/mvp1-tools-start from main, hygiene next, land per dev-workflow.
- Verify: uv run ... --use-tools works (emits, acts), pytest new tests green.
- Cross-cite: plan.md §1 (B1 tool host v0 + B2 loop + integrate tero/W2), wsfull compact, WORKSPACE..., prior agents--pr12...
- Status: MVP-1 started (minimal functional). Full B3+ (config/verify) later. No overclaim.

## MVP-1 complete (chore/cabal-poc-mvp-close appended)
- B1/B2 done + verified green: tools.py full host+parse+safe+events; agent loop tool detect/execute/re-prompt budget + feedback; cli --use-tools + events; prompt inject; 4 new tests + 6 prior (10 pass).
- Exec verified (parse, list/read/run host, agent loop with mock tool-then-answer).
- Integrates W2 Structured + tero memory in same loop (no breakage to non-tool path).
- Per plan.md cabal-poc-mvp + ROADMAP Wave B; cross-cites wsfull compact, OPEN_ISSUES (MVP-1 section), PHASE, AGENTS, dev-docs readiness.
- Tero-first + hygiene + update-tero post; land --no-ff dev/main + propagate.
- MVP-1 acceptance met (see OPEN). Defer B3 config, B4 verify/iter feedback, TUI polish etc.
- Tero cite: roadmap--mvp-1-complete...


---

### Wave C — Daily co-dev polish (MVP complete)

**Goal:** Comfortable daily driver.

| ID | Work |
|----|------|
| C1 | Notifications: Discord webhook + Telegram (PHASE) |
| C2 | `uv tool install` / packaging smoke |
| C3 | Human-in-the-loop: `NEEDS_HUMAN_INPUT` event + TUI/CLI prompt |
| C4 | Richer Tero use: `query_by_id`, `cross_ref` when task mentions IDs |
| C5 | Multi-provider ABC second impl (e.g. Anthropic) — can slip to D |
| C6 | Resource soft limits: max tokens, max tool calls, timeout (hooks for PROD) |

**Exit:** PHASE MVP exit criteria met; Production items still deferred.

---

### Wave D — Multi-agent & production shape

**Goal:** Coordinated agents with safe concurrency; security load-bearing.

| ID | Work | Corpus alignment |
|----|------|------------------|
| D1 | **Wave executor** | Port *pattern* of mycelium `wave` skill: partition by file ownership, one worktree per leaf agent |
| D2 | **Lowest-common-owner merge** | Shared files escalate to parent orchestrator (DN-87 §5 / CLAUDE fractal swarm) |
| D3 | **Orchestrator agent** | Sequential/parallel/loop composition inspired by RFC-0023 §3.5 (Python, not Mycelium ADK) |
| D4 | **Discord control plane** | Submit tasks, monitor, approve |
| D5 | **Security tool wrappers** | Hardwired allowlists; optional Security MCP; gitleaks-aligned |
| D6 | **Tero Layer-2 consumer** | Only when M-1018 / full tero ships Empirical gains; until then stay L1 |
| D6b | **Real RAG (if not Tero L2)** | Only if context-mcp (or successor) ships **real embeddings + vector store** and passes an Empirical eval — **pseudo-embeddings do not count** |
| D7 | **Persistent multi-session state** | Resume swarms, budgets, audit log (JSONL and/or context-mcp **as KV session store**, not as RAG) |

**Exit:** PHASE Production exit criteria.

## Wave Updates (W2 Facade + Cabal Integration, 2026-07-09)

As part of wsfull PR process and doc/tero updates:

- W2 CommonMemory facade implementation + AgentDomain M1: CommonMemoryAdapter (query returns cited StructuredResponse; domains TERO etc), Structured* W2 schemas in core/schemas.py (codegen'd from dev-docs/schemas/).
- Wiring in agent (prompt/agent/tero_client): facade primary for tero queries + memory_contexts in run_structured; supports W2 orch.
- PR #12 (cab/a1-a3-tui-errors-tests → dev): facade, A1-A3 (TUI/errors/tests), integration, doc updates (incl. this, AGENTS, INTENT, PHASE, TERO, README, .claude/kickoffs/README.md), tero reindex.
- Kickoffs, agent context (AGENTS.md), claude files updated to latest (facade, W2 schemas, tero-first, dev-workflow, branch/worktree guards, hygiene, C0/M1).
- Tero indexes run post-docs (via /root/git/scripts/update-tero.sh cabal-devmelopner), committed to PR.
- Integration via cabal, tero: local tero discovery; full workspace targets per WORKSPACE_CABAL_TERO_READINESS.md; hygiene/security applied.
- Reviews via pr-review skill (adapted: emphasize tero citations, W2/StructuredResponse, CommonMemory facade, C0 honesty gate, M1 domains from memory-gate, dev-workflow, guards, hygiene/security, append-only, tero-first, parameterized skills); if positive no critical blockers, merge with gh pr merge --auto.
- State from wsfull-wave-2026-07-09-compact.md (deliverables: W2 facade, C0/M1 leafs, local models, skills, hygiene), WORKSPACE_CABAL_TERO_READINESS.md (W2 facade cabal integration post-wave, parameterization).
- Docs + tero always updated in PR process (tero-first before edits). Gaps in OPEN_ISSUES. Follow dev-workflow for authoring.

See AGENTS.md for tero-first + facade usage.

---

## 5. Dependency graph (high level)

```text
Wave A (PoC honest)
    │
    ▼
Wave B (tools + config + verify + TUI v1)
    │
    ├──────────────► Wave C (polish, notify, HITL)
    │
    ▼
Wave D (swarm / security / multi-provider / L2 Tero)
```

Within Wave A, A1–A4 parallelizable; A5 after; A7 after A5.  
Within Wave B, B3 early; B1→B2→B4 chain; B6 parallel after A1.

---

## 6. PR Plan (incremental, reviewable)

Each PR should be independently mergeable to `dev`. Suggested titles match GitHub issues where they exist.

### Wave A

| PR | Title | Scope | Depends |
|----|--------|--------|---------|
| **PR-A1** | `fix(tui): add main entrypoint for cabal-devmelopner-tui` | `tui/app.py` `main()`, optional `__main__.py` | — |
| **PR-A2** | `fix(tui): use Task dataclass` | TUI task construction | PR-A1 optional |
| **PR-A3** | `fix(agent): surface Tero and provider errors via EventBus` | agent.py, events | — |
| **PR-A4** | `test: expand PoC smoke coverage` | EventBus, prompt, Tero mock, CLI | PR-A3 nice |
| **PR-A5** | `ci: run pytest on push/PR to dev and main` | `.github/workflows/` | PR-A4 |
| **PR-A6** | `chore: declare textual/runtime dependency story` | pyproject.toml | — |
| **PR-A7** | `docs: finalize PoC exit notes after A1–A6` | PHASE, OPEN_ISSUES, INTENT | after A1–A6 |

### Wave B

| PR | Title | Scope | Depends |
|----|--------|--------|---------|
| **PR-B1** | `feat(tools): tool host v0 (read/list/run)` | `core/tools/`, types | Wave A |
| **PR-B2** | `feat(agent): tool loop with step budget` | agent.py, prompt | PR-B1 |
| **PR-B3** | `feat(config): workspace + model + tero config file` | `core/config.py` | Wave A |
| **PR-B4** | `feat(agent): verification command feedback` | agent, config | PR-B2, PR-B3 |
| **PR-B5** | `feat(tui): live status, cancel, real Task wiring` | tui/ | PR-A1, PR-B2 |
| **PR-B6** | `feat(provider): streaming completions` | xai.py, events | PR-B5 optional |
| **PR-B7** | `feat(session): transcript JSONL` | core/session | PR-B2 |
| **PR-B8** | `feat(tero): richer queries + missing-path errors` | tero_client, agent | PR-A3 |

### Wave C

| PR | Title | Scope |
|----|--------|--------|
| **PR-C1** | `feat(notify): Discord webhook + Telegram` | `notify/` |
| **PR-C2** | `feat(cli): human-in-the-loop approval` | events, CLI/TUI |
| **PR-C3** | `chore(packaging): uv tool install path` | pyproject, docs |
| **PR-C4** | `feat(provider): second backend` | providers/ |

### Wave D

| PR | Title | Scope |
|----|--------|--------|
| **PR-D1** | `feat(swarm): wave partition + worktree leaves` | `swarm/` |
| **PR-D2** | `feat(swarm): LCO merge policy` | swarm + docs |
| **PR-D3** | `feat(discord): control plane` | surfaces |
| **PR-D4** | `feat(security): tool allowlist + wrappers` | tools, security |
| **PR-D5** | `feat(tero): Layer-2 client when upstream ready` | mcp/ |

---

## 7. Key decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **PoC multi-iteration** | Defer real loops until tools (Wave B); docs stay honest | Feedback without verification is theater |
| **Tero role** | L1 corpus context now; never claim RAG; L2 only post M-1018 Empirical | DN-87 honesty posture |
| **Two Tero paths** | Keep Grok MCP (session) separate from in-process client; same binary/index | Cold-start docs already capture this |
| **Tools before Discord** | Wave B tools ≫ Wave C notify | Product is a *dev agent*, not a chat relay |
| **Swarm pattern** | Copy *process* from mycelium `wave` skill, not Mycelium runtime | Repo-agnostic Python product |
| **ADK / RFC-0023** | Conceptual inspiration only; no dependency on mycelium-adk | M-671 blocked; cabal must ship independently |
| **Security** | Allowlists + event audit in MVP; full Security MCP in D | PHASE note: consider early, implement fully later |
| **Python version** | Stay on project pin (3.14) until packaging forces broader | Avoid drive-by churn |

---

## 8. Open questions (need maintainer input)

1. **Default tool allowlist** — shell unrestricted vs allowlist-only from day one? (Recommend allowlist-only.)
2. **Config format** — TOML vs YAML vs env-only for v0? (Recommend TOML.)
3. **Second provider priority** — Claude vs OpenAI-compatible first?
4. **Discord vs Telegram first** for notifications?
5. **Index portability** — should cabal learn to *build* a Tero index for arbitrary repos (tero-mcp GENERATING-AN-INDEX), or only consume existing indices until later?

---

## 9. Suggested near-term execution order (next 2 weeks)

1. Land docs PR #1 (intent/gap + cold-start) if not merged.  
2. **PR-A1 + PR-A2** (TUI works) — unblocks dogfooding.  
3. **PR-A3 + PR-A4 + PR-A5** (errors + tests + CI).  
4. **PR-B1 + PR-B2** (tools + loop) — product becomes a real agent.  
5. **PR-B3 + PR-B4** (config + verify).  
6. **PR-B5** (TUI v1) in parallel once A1 landed.

---

## 10. Success metrics (lightweight)

| Phase | Signal |
|-------|--------|
| PoC exit | TUI launches; pytest CI green; no false “done” checkboxes |
| MVP exit | End-to-end: task → tools → tests → result on a real repo weekly |
| Production | Multi-agent wave completes without silent merge conflicts; security gates block unsafe tools |

---

## 11. References (Tero-cited)

| Ref | Path / id | Use in this plan |
|-----|-----------|------------------|
| DN-87 | `docs/notes/DN-87-…` (mycelium) | Tero L1/L2, honesty, API shape |
| M-1015 | done — Layer-1 index | Default index consumer |
| M-1017 | todo — MCP/HTTP fronts | Align client maturity |
| M-1018 | Layer-2 + eval | Gate PROD-6 |
| wave skill | `.claude/skills/wave/SKILL.md` | Wave D executor |
| RFC-0023 §3 | Agent/Tool/Session/Multi-agent | Conceptual model |
| E22-1 | Security scanning toolkit epic | Security direction |

Local product docs: PHASE, INTENT_AND_GAP_ANALYSIS, OPEN_ISSUES, TERO.

### Appended: PR#12 W2 facade + C0 resolution (2026-07-09)
- Integrated W2 schemas (Structured*, Citation, MemoryContext) + CommonMemoryAdapter + AgentDomain M1 (6+ domains incl. TERO/CONTEXT/MEMORY_GATE/LANG_*).
- Agent uses facade for tero-first context in StructuredResponse. C0 fix: ERROR emitted on facade tero fails.
- Doc updates + kickoffs + AGENTS + tero reindex part of PR process.
- Next: pr-review (one agent, adapted rubric), merge to dev, then main + pull-down propagate.
- Grounded in wsfull-wave-2026-07-09-compact.md (Tero: workspacecabalteroreadiness sections), dev-workflow, guards.

### Honest docs update (chore/honest-docs-post-w2)
- Aligned lagging current-position table + Wave A exit text post-PR#12 merges (TUI entrypoint now accurate; POC-1/3/4 closed in code).
- POC-6 (iteration) kept as partial per reality (early-return in agent loop).
- Cross-cites wsfull-wave-2026-07-09-compact.md + WORKSPACE_CABAL_TERO_READINESS.md + PR#12. Append-only section.
- Tero-first queries ("W2 Facade", "C0", "wsfull-wave") + cited reads before edits. No src changes. See PHASE/OPEN_ISSUES/INTENT for matching.
- Follows: main pull, chore branch, check.sh, signed commit, PR to main. Tero cite: agents--pr12-review-merge-2026-07-09.

### POC-6 documented single-shot (chore/poc6-iteration-honesty per plan.md p2)
- A6 marked documented single-shot; footnote updated; exit/position text revised for honesty (no longer requires POC-6 for PoC exit).
- Decision: single-shot is the honest state; full iteration/feedback + verify deferred until tools land (MVP-1, Wave B B4 verification hook).
- Cross-cites: plan.md (cabal section §1: "POC-6 (P1)... document single-shot (honest)..."; "Start with POC-6 decision"), wsfull-wave-2026-07-09-compact.md, PHASE.md (updated), WORKSPACE_CABAL_TERO_READINESS.md, AGENTS.md.
- Tero-first (script text_search "POC|plan|wsfull" + MCP identify) + cited reads of plan + prior phase/intent hits before edits. Refusals on exact "POC-6" pre this (expected).
- Append-only + targeted accuracy. Branch from main. Will run update-tero post.
- Tero cite post: roadmap--wave-a... + new section. Follows dev-workflow/append-only/guards.

### dev-mcp Orch Wiring (cabal as leaf consumer; chore/orch-wiring-devmcp)

Appended notes on dev-mcp orch use per task (parallel to W2 docs):

- cabal-devmelopner = leaf for dev-mcp tasks: consumes dev-mcp inventory (servers/README, top README), registers family MCPs, executes as consumer in orch (W2 facade for memory across tero/agent-mcp/context/memory-gate).
- W2 facade matrix + memory-gate domains (M1): referenced in cabal's CommonMemoryAdapter (AgentDomain.TERO primary for tero-first + orch); see enhanced dev-mcp/servers/README.md#orch-inventory-truth (table of consumers/domains) + cabal schemas.py .
- Links added in dev-mcp: to cabal AGENTS/ROADMAP, leaf ROADMAPs; doctor notes fit.
- From dev-mcp ROADMAP: advances D-B2 (cabal consumption matrix), D-A inventory truth (cabal marked # consumer).
- Orch vision tie: cabal as executor leaf in single-NL / wave orch (plan.md §3, wsfull kickoff); uses dev-mcp for cross-family map.
- Tero cites (MCP/script pre-edit): dev-mcp text_search "orch|inventory|w2|cabal" (anchors: readme--server-inventory, memory-gate-rs--w2-mirror..., workspacecabalteroreadiness--leaf-orch-review-tranche-wsfull); cabal text_search "dev-mcp orch w2" (agents--..., roadmap--wave...); explain/cite used.

See dev-mcp/docs/ROADMAP.md (orch section), servers/README.md (matrix), plan.md §3. 

Append-only; hygiene (check.sh), update-tero, branch chore/orch... Land --no-ff + propagate to verify tero "dev-mcp|orch|leaf". Cross: AGENTS.md (this append), WORKSPACE_CABAL..., wsfull compact.
