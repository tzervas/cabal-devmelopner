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

## 2. Current position (summary)

| Area | State |
|------|--------|
| CLI + xAI one-shot | Works |
| EventBus + Provider ABC | Seams ready |
| Tero client + docs + Grok cold-start | Usable with siblings; opt-in |
| TUI | Code present; **entrypoint broken** (POC-1) |
| Agent loop | Single-shot; multi-iteration dead (POC-6) |
| Tools / verify / multi-agent | Not started |

**PoC exit** requires P0 TUI launch + honest tests/stabilization. **MVP exit** requires tools + verification + usable TUI/config. **Production** is multi-agent + security + resources.

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
| A6 | Multi-iteration honesty | #5 POC-6 | product choice* |
| A7 | pytest CI workflow | #7 MVP-4 | A5 |
| A8 | Runtime deps honesty (`textual` extra) | MVP-3 | — |

\* **A6 choice:** either (i) document single-shot and keep PHASE `[~]`, or (ii) one cheap verification signal (e.g. non-empty + optional self-check prompt) before exit. Prefer (i) until tools exist, then real feedback in Wave B.

**Exit:** `uv run cabal-devmelopner-tui` works; `pytest` green in CI; PHASE PoC partials only for intentional deferrals.

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
