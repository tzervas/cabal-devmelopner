# Agent notes — cabal-devmelopner

Operator-style rules for solo AI **and** multi-agent L0/L1 (fractal) waves.
Living file: **append** status sections; keep this top block accurate.

## Product (alpha 0.1.x)

- **Role:** repo-agnostic development agent (CLI/TUI), leaf executor in swarms
- **Config:** `cabal.example.toml` → optional `cabal.toml` (profiles **l1** default, **l0** frontier)
- **Compose:** [docs/COMPOSE.md](docs/COMPOSE.md) — tz-forge `agent-swarm` + agent-harness + tg-agent-relay
- **Assistant context:** [CLAUDE.md](CLAUDE.md)
- **Honesty:** not full multi-agent production; tools MVP-1; Tero opt-in; **no mycelium automation**

## Fractal model policy (L0 / L1)

| Role | Class | Default | Use for |
|------|-------|---------|---------|
| **L0** | Frontier | Named only when architecture is hard | Design forks, irreversible naming, cross-repo program design |
| **L1** | Composer / fast implementer | **Default for all implementation** | Code, tests, docs, PRs, config, evidence |

- Select via `cabal.toml` `agent.profile` or CLI `--profile l0|l1`
- **No automatic Copilot code review** (fleet-wide)
- Wave shape: optional L0 design → L1 implement leaves → L1 pr-review → merge (`Refs` on dev, `Closes` on main)

## Local gates

```bash
./scripts/check.sh
./scripts/check.sh --quick
./scripts/check.sh --fix
uv run cabal-devmelopner --version
uv run pytest -q
```

## Branch / PR guards

- Branch from `dev`; never commit directly to `main`
- Feature → `dev`: **`Refs #n`** only (issues stay open)
- Delivery → `main`: **`Closes #n`** / **`Fixes #n`**
- Prefer one worktree per concurrent wave
- Append-only for this file + ROADMAP/PHASE status sections

## Tero (documentation / corpus context) — now dynamic over tero-rs

Use **Tero** (Python presenter over tero-rs binary) for cited lookups. The surface (tools, args, inputSchemas with Rust type hints, categories: introspection/query/explain/maintenance) is **dynamically discovered** at runtime via `--describe`. Python renders (loose hints + early schema validation + rich errors); Rust backend ensures strict validation + execution + Layer-2 when gated.

Prefer tero before greps. Full guide: **[docs/TERO.md](docs/TERO.md)**. Categories help smart scoping (e.g. query tools for cross-repo relevant knowledge without bloat).

See workspace vision for common memory (tero + context-mcp + memory-gate-rs), local llama.cpp/GPU, cross-repo scoped reuse, token optimization.

**Kickoff framework**: root `.claude/kickoffs/cab.md` + `wsfull.md` owns the work here. Use fresh `/kickoff cab`. Apply partial mycelium workflow (dev-workflow, tero-first with categories, guards, wave). Local `.claude/kickoffs/README.md`. **Do not automate mycelium clone/update from this product.**

### Prefer

1. `text_search` / `query_by_id` / `query_by_kind` via the **tero** MCP server (when registered in Grok).
2. Open the **cited file:line** — treat hits as pointers, not ground truth.
3. On refusal (`kind: refusal` / no citable match), rephrase or fall back to normal repo search.

### Subagents and multi-repo excavation (required when Tero is available)

Sibling-tool investigations, readiness audits, and design waves are **harder** if agents only `ls`/`grep` checkouts. **Every agent that excavates** (orchestrator *and* leaf subagents) should use Tero first for corpus memory, then verify against local trees.

**Orchestrator checklist when spawning investigation agents:**

1. Confirm `tero__identify` (or `search_tool` → `tero__*`) works; if not, follow cold-start below before launching a wave.
2. Put an explicit **Tero excavation block** in every subagent prompt (copy below). Do not assume the child will invent it.
3. Prefer leaf prompts that name **ids to chase** when known (`DN-87`, `M-1017`, RFC/ADR numbers, skill names).
4. After leaves return, orchestrator may `cross_ref` / `query_by_id` on any new ids the leaves surfaced.

**Paste into each investigation subagent prompt:**

```text
## Tero excavation (do this before deep filesystem greps)

You have access to the `tero` MCP server (tools `tero__*`). Use it to excavate project
memory related to your target. Token: "local-dev" (or env TERO_TOKEN).

1. search_tool query="tero" once if needed to refresh schemas.
2. tero__identify { "token": "local-dev" } — confirm index is live.
3. tero__text_search { "value": "<target name + MCP/security/agent keywords>", "token": "local-dev" }
4. For each strong hit with an id (DN-…, M-…, RFC-…, E…): tero__query_by_id
5. tero__cross_ref { "start": "<id>", "depth": "2", "token": "local-dev" } when mapping programs
6. Open cited file:line paths under the mycelium (or other) tree — summaries are not ground truth.
7. Only then dig the local sibling checkout (branches, README, src, tests).

If tero__* tools are missing: note "Tero unavailable" in the report and fall back to repo search;
tell the orchestrator to fix MCP registration for the next wave.
```

**Why:** The Mycelium index holds decisions, issues, and skills that explain *why* a sibling MCP exists and what “done” means. Local clones alone miss paused design intent and cross-repo links.

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

## Latest State (W2 Facade + Integration, 2026-07-09)

- W2 CommonMemory facade implementation: CommonMemoryAdapter + AgentDomain M1 (full Py mirror of memory-gate-rs M1 domains with prefix parsing: GENERAL, TERO, CONTEXT, MEMORY_GATE, LANG_RUST, LANG_PYTHON, WORKSPACE, INFRASTRUCTURE etc.) landed in core/schemas.py (from codegen + dev-docs/schemas/common_memory_facade + W2-STRUCTURED-SCHEMAS.md).
- Wired in agent: SimpleAgent (core/agent.py) uses self.facade.query(AgentDomain.TERO, ...) in run_structured to drive memory_contexts + last StructuredResponse (W2: StructuredResponse with citations, MemoryContext, explain); StructuredPrompt for prompt builder. Legacy tero_client path compat preserved. Errors via EventBus (never silent, C0).
- Supports domains for scoped: TERO (primary), CONTEXT, MEMORY_GATE, LANG_*, WORKSPACE etc. for cabal integration.
- PR #12: cab/a1-a3-tui-errors-tests → dev (facade + wiring + A1-A3 TUI/errors/tests + docs + tero).
- Integration via cabal, tero: tero_client auto-discovers local docs/tero-index; facade primary for queries in agent; full workspace (dev-docs readiness post wsfull).
- Hygiene, C0/M1: applied per leaf (C0 honesty gate on context-mcp, M1 on memory-gate); cabal: ruff, checks, parameterized hygiene/security.
- Kickoffs, agent context (this AGENTS.md), claude files (.claude/kickoffs/README.md) updated to latest: facade refs, W2 schemas/StructuredResponse, tero-first, dev-workflow, branch/worktree guards, append-only.
- Use: `uv run cabal-devmelopner "..." --use-tero --local-model ...` (prefers local-ollama + tero + W2 Structured); TUI with USE_TERO.
- Docs (AGENTS, README, ROADMAP, INTENT_AND_GAP_ANALYSIS, TERO, PHASE, kickoffs) + tero updated as part of PR process.
- See: wsfull-wave-2026-07-09-compact.md (deliverables: W2, local models, hygiene, C0/M1, parameterized skills), WORKSPACE_CABAL_TERO_READINESS.md (facade integration, tero indexing, dev branches).
- Tero-first, dev-workflow, guards (branch-guard, worktree-guard) followed. After edits: hygiene --reload, update-tero.sh, tero search.
- Next: PR review (pr-review skill adapted), merge --auto if no blockers, propagate.

Update this file + kickoffs + tero after any changes. Tero-first always (use script or MCP). Cite tero: e.g. agents--latest-state-w2-facade-integration-2026-07-09.

## Post C0 Fix for PR#12 (2026-07-09, appended)

- CRITICAL blocker resolved: in CommonMemoryAdapter.query (schemas.py) tero backend error returned as explicit StructuredResponse.refusal (per facade contract + W2 honesty), but agent.run_structured did not surface to EventBus.ERROR when facade path used (because query never raised; legacy elif unreachable since __init__ wires facade from tero_client).
- Fix (C0 "never silent" + POC-4/A3): in agent.py, after facade.query, if sresp.is_refusal() then emit EventType.ERROR with "CommonMemory facade error: ..." using detail from extended["error"] or answer. This ensures observability for tero fails (UIs, tests, logs) while facade keeps "always StructuredResponse" contract.
- Updated test_tero_error_emits_event (tests/test_smoke.py): now asserts "CommonMemory facade error" / "facade query failed"; docstring updated to reflect facade+agent responsibility for ERROR emit.
- Verified: direct pytest equiv + ruff format/lint + checks pass (test_tero_error_emits_event + provider error path both green).
- This closes the last C0 violation in the facade wiring tranche. PR#12 now clean for re-review/merge.
- Tero cites (from prior): workspacecabalteroreadiness--w2-structured-schemas-orch-started-2026-07-08 etc. See dev-docs/waves/wsfull-wave-2026-07-09-compact.md §Post-Review + swarm status.
- Followed: dev-workflow (small targeted edit + test first), append-only, branch-guard (on cab/...), tero-first (cited before edit).
- After: will run update-tero.sh cabal-devmelopner ; commit to branch (included in PR#12); then pr-review + merge.

Tero-first + update-tero after all doc edits. Guards respected.

## PR#12 Review+Merge Agent (2026-07-09 appended)

- Tero-first (MCP + script): tero__identify + text_search "cabal W2 facade" "C0 PR#12" "dev-docs wsfull-wave-2026-07-09-compact" (hits: workspacecabalteroreadiness--w2-facade-cabal-integration-post-wsfull-wave-2026-07-09-compact line~103, agents--post-c0-fix-for-pr12-2026-07-09-appended:129, phase--appended-w2-c0-fix-for-pr12-2026-07-09 etc). /root/git/scripts/tero.sh also run (150 items scanned).
- pr-review/SKILL.md + _shared/review-rubric.md read. Triage: T2 (18 files, +1361 LOC, honesty/C0 surface, W2 contract touch in schemas/agent).
- Diff: gh pr diff 12 + git diff f2c0bef^..7c7e47e . Intent from body: W2 facade+AgentDomain wiring, StructuredResponse, C0 fix.
- Checklist (grounded file:line):
  - Correctness: facade returns always StructuredResponse (refusal on err, schemas.py:399); agent emits ERROR on is_refusal() (agent.py:85-98 "CommonMemory facade error") + except path. test_tero_error_emits_event + provider test pass (.venv/bin/python -m pytest green).
  - Honesty/C0: no silent (removed old except:pass); ERROR on facade/tero/provider errs. W2: StructuredResponse always kind+answer or explicit refusal (is_refusal, refusal()).
  - M1/W2: AgentDomain (schemas.py:317) mirrors memory-gate (prefix from_str for TERO/CONTEXT/MEMORY_GATE/LANG_* etc); CommonMemoryAdapter (369) domain query + citations + StructuredResponse.
  - dev-workflow/guards/append-only/hygiene/tero: branch cab/a1-a3 (pre), append sections in AGENTS/README/ROADMAP/PHASE/INTENT/TERO/kickoffs, ruff+checks pass, update-tero included (150 items).
  - Recent commit 7c7e47e (C0 fix + test) included in PR tip.
- Report per rubric §4 emitted + posted as gh pr comment (https://github.com/tzervas/cabal-devmelopner/pull/12#issuecomment-4925135941). PR body edited to note C0+review+ cites.
- Merged: gh pr merge 12 (state MERGED).
- Post-merge: git checkout dev; (pull attempted); /root/git/scripts/update-tero.sh cabal-devmelopner; hygiene (ruff+6 tests green).
- Updated remaining: appended this section (AGENTS.md) + note to cab.md (root .claude); re-ran update-tero.
- No blockers. Status: landed. Use: uv run cabal-devmelopner "..." --use-tero --local-model.

All per AGENTS, wsfull-wave-2026-07-09-compact.md, dev-workflow. Tero cite: agents--pr12-review-merge-2026-07-09.

### Honest docs closure (chore/honest-docs-post-w2, 2026-07-09 appended)
- Tero-first (MCP identify + text_search "W2 Facade"|"C0"|"POC"|"wsfull-wave" + cite reads of dev-docs/waves/* + WORKSPACE... before greps/edits). Read cited + PHASE/OPEN_ISSUES/ROADMAP/INTENT/AGENTS/README.
- Aligned lagging PoC/TUI/Tero/iteration status text (checkboxes, tables, narrative) across PHASE/ROADMAP/OPEN_ISSUES/INTENT/README to match post-PR#12 code reality (A1-A3 + C0 facade ERROR landed+merged; iteration partial).
- Append-only sections + targeted accuracy fixes (conservative: no overclaim on iteration/tests/TUI polish).
- Cross-cites wsfull-wave-2026-07-09-compact.md, WORKSPACE_CABAL_TERO_READINESS.md, PR#12.
- Process: main pull; git checkout -b chore/honest-docs-post-w2; edits; scripts/check.sh --quick; commit -S; push + gh pr --base main.
- After: update-tero.sh cabal-devmelopner; hygiene. Tero cite for this: agents--pr12-review-merge-2026-07-09 + workspacecabalteroreadiness--*. Follow AGENTS dev-workflow, branch-guard, append-only. Update this + kickoffs + tero on changes.

### POC-6 iteration documented single-shot (chore/poc6-iteration-honesty appended 2026-07-09)
- Tero-first (required): /root/git/scripts/tero.sh cabal-devmelopner text_search "POC-6|iteration" (refusal, 156 rows, no prior match); re-ran for "POC","plan","wsfull"; MCP: search_tool "tero", tero__identify, tero__text_search "POC-6" etc (refusals pre), "cabal"/"plan" hits (workspacecabalteroreadiness sections). Excavation before any greps/edits + reads of cited.
- Read: plan.md (cabal section p2 on cabal-poc-mvp POC-6), docs/OPEN_ISSUES.md, PHASE.md, ROADMAP.md, AGENTS.md (this), + wsfull compact.
- Branch: git checkout -b chore/poc6-iteration-honesty (from main, clean).
- Decision per task/plan: document POC-6 as single-shot (honest); defer full feedback/iter to MVP/tools (no code change).
- Updates (append-only + targeted marks for status): PHASE.md (deliverables bullet + exit criteria + new append section), ROADMAP.md (A6 row + footnote + exit text + append), OPEN_ISSUES.md (status list + new append), INTENT_AND_GAP_ANALYSIS.md (priority + bottom line + append), AGENTS.md (this).
- Cross-cites: plan.md ("POC-6 (P1): ... document single-shot (honest, defer full feedback to MVP/tools). Update PHASE/ROADMAP/OPEN_ISSUES/INTENT/AGENTS (append-only, cross-cite wsfull compact + this plan)."), wsfull-wave-2026-07-09-compact.md, WORKSPACE_CABAL_TERO_READINESS.md, prior tero hits e.g. phase--honest-poc..., intentandgapanalysis--8.-recommended..., roadmap--wave-a...
- Commit: signed -S "docs(poc6): document iteration as single-shot honest (plan.md p2)"
- Then: ./scripts/check.sh (or ruff/pytest), /root/git/scripts/update-tero.sh cabal-devmelopner ; verify tero hits; pr-review if avail (follow merge); land: git checkout dev; git merge --no-ff ... ; push; main --no-ff; propagate.
- Follows exactly: AGENTS (Tero excavation block, prefer tero before greps, subagent rules, dev-workflow, guards, append-only, update this+tero+kickoffs), hygiene, C0/M1 honesty. No overclaim.
- Tero cite: agents--poc6-iteration... + plan refs. Post: re-run update-tero + text_search "POC-6".

### MVP-1 minimal tools start (chore/mvp1-tools-start appended 2026-07-09)
- Task: start MVP-1 per plan.md p2 cabal-poc-mvp (parallel to w2): B1 tool host v0 (read_file/list_dir/run_command allowlisted + TOOL_* events), B2 loop (model propose/execute/re-prompt limited), integrate tero/W2.
- Tero-first (script + MCP): /root/git/scripts/tero.sh cabal-devmelopner text_search "MVP-1|tool|read_file" (refusals pre + hits on mvp/tool sections in docs); tero__identify, tero__text_search "MVP-1 tools B1..." (workspacecabal... + roadmap mvp + phase mvp + openissues p2); repeated before branch/edits/greps.
- Read (after tero): plan.md (cabal MVP B1/B2), agent.py/event.py/types.py/schemas.py (W2 StructuredResponse + pre-existing TOOL_*), test_smoke.py, cli.py, prompt.py, ROADMAP/OPEN_ISSUES/PHASE/AGENTS.
- Branch: git checkout -b chore/mvp1-tools-start (from main, per task; guard respected).
- Impl (minimal):
  - New: core/tools.py (ToolHost, parse_tool_call, safe read/list/run_command w/ allowlist, emit TOOL_CALL/RESULT, get_descriptions, confine to workspace_root).
  - agent.py: import, __init__ (tools_enabled, ToolHost), run_structured loop (parse after gen, exec+feedback+continue for re-prompt if tool; compat !tools path + early return preserved; W2/tero unchanged).
  - prompt.py: always-inject tool format/desc (MVP start) so model can propose; StructuredPrompt used.
  - cli.py: --use-tools flag, subscribe TOOL_* (print), pass to agent + workspace_root="".
  - tests: parse, host (tmp+allow), agent tools loop (mock tool-then-final, asserts events + multi-call + final resp).
- Docs (append-only + targeted): ROADMAP (new MVP-1 section + B table context), OPEN_ISSUES (MVP-1 row + new status append), PHASE (MVP bullet + append), AGENTS (this).
- Hygiene: will run scripts/check.sh (ruff/pytest), update-tero.sh cabal-devmelopner.
- Land: commit -S, PR if, --no-ff to dev then main, propagate pulls, reindex tero.
- Verify per task: cabal --use-tools runs (emits, acts on read/list), tero hits post, tests green (incl new).
- Follows: AGENTS (Tero excavation block in this, prefer tero, dev-workflow, guards, append-only, update this+tero+kickoffs after), C0 (events never silent), M1/W2 (Structured + facade untouched).
- Cross-cites: plan.md, roadmap--wave-b-minimum..., openissues--mvp-1..., phase--mvp..., workspacecabalteroreadiness (prior), wsfull-wave-2026-07-09-compact.md, prior agents--poc6...
- Tero cite: agents--mvp1-tools-start-2026-07-09 (post update-tero.sh).
- Note: this starts MVP-1 (parallel w2); POC-6 still single-shot honest until B4 verify. No overclaim on full iter.

Follow AGENTS exactly on future changes.

## dev-mcp Orch Use (cabal as leaf for dev-mcp tasks; chore/orch-wiring-devmcp appended)

cabal-devmelopner is the leaf consumer/executor for dev-mcp orch tasks:

- Discovery + onboarding: use dev-mcp README + servers/ for family inventory (agent-mcp orch, tero L1, memory-gate domains M1, context session, security). Clone/register via AGENTS.md snippets there.
- W2 facade matrix: cabal implements CommonMemoryAdapter + AgentDomain (mirror memory-gate-rs) as primary consumer; domain-scoped queries (TERO etc) feed StructuredResponse (citations + orchestration) for cross-family orch (see dev-mcp servers/README.md#orch-inventory-truth for matrix).
- dev-mcp tasks: cabal acts as leaf executor (tools loop + tero/W2 in agent); dev-mcp indexes cabal as "consumer". See family clone layout in dev-mcp/README.md.
- Links: dev-mcp servers/README.md (enhanced with links + doctor notes), docs/ROADMAP.md (Wave B cabal matrix), docs/ASSESSMENT.md; per-server e.g. memory-gate-rs.md, agent-mcp.md.
- Doctor: grok mcp doctor tero (or per-server); cabal --use-tero exercises dev-mcp family paths.
- Orch hints: facade supports dev-mcp orch wiring (plan §3); future agent-mcp will consume cabal W2 outputs.

Tero-first (pre + post): MCP tero__text_search "dev-mcp orch w2 facade" + /root/git/scripts/tero.sh dev-mcp "orch inventory w2 cabal" (hits: memory-gate-rs--w2-mirror-to-cabal-tero, readme--server-inventory, workspacecabalteroreadiness sections, agents--subagents...); cite used.

Cross-cites: plan.md §3 orch-wiring, dev-mcp ROADMAP (D-B2), wsfull-wave-2026-07-09-compact.md, WORKSPACE_CABAL_TERO_READINESS.md (leaf-orch), dev-mcp servers/README post-update.

Append-only; followed dev-workflow, branch-guard (chore/orch-wiring-devmcp), hygiene + update-tero. Land --no-ff dev/main + propagate. Verify tero hits "dev-mcp|cabal as leaf|orch".

Update this + kickoffs + tero after.


## P28b production polish (feat/p28-production appended 2026-07-16)

- **Bar:** plans/fractal/P28_AI_DEVTOOLING_PRODUCTION.md Wave A cabal-devmelopner
- Delivered:
  - Config-as-code: `cabal.example.toml` + `core/config.py` (L0/L1 profiles, tero-first, no mycelium automation); CLI wire (`--config`, `--profile`, `--version`)
  - CLAUDE.md + fractal top of this AGENTS.md
  - README 5-min: setup.sh → `--version` / pytest / check.sh; tero sibling optional
  - docs/COMPOSE.md: tz-forge agent-swarm + harness + relay + tero
  - CHANGELOG.md + VERSION 0.1.0 (alpha honest)
  - tests/test_config.py; local check green
- Branch: `feat/p28-production` → PR → merge to `dev` (Refs only; Closes on main later if needed)
- Evidence: `/root/work/plans/evidence/P28-ai-devtooling/P28b-cabal.md`
- Non-goals: no mycelium automation; no false production claims; no Copilot auto-review

Update this + tero after material process changes.
