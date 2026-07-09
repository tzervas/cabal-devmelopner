# cabal-devmelopner — Tero Index (Layer 1)

> **Honesty:** Empirical/Declared — lite heading/line heuristic over markdown in cabal-devmelopner via tero-mcp/scripts/generate_lite_index.py; source files are ground truth. Generated 2026-07-09.
> Use this index to find where to Read, not as authoritative ground truth.

- **Items:** 165
- **Flagged:** 0
- **item_tag:** `Empirical/Declared`
- **Machine index:** [`index.json`](./index.json)
- **Manifest:** [`MANIFEST.toml`](./MANIFEST.toml)

## doc (165 entries)

| Anchor | Kind | Id | Title | File:Line | Status | Summary |
|---|---|---|---|---|---|---|
| `agents` | section | — | Agent notes — cabal-devmelopner | `AGENTS.md:1` | — | Use Tero (Python presenter over tero-rs binary) for cited lookups. The surface (tools, args, inputSchemas with Rust type hints, categories: introspection/query… |
| `agents--tero-documentation-corpus-context-now-dynamic-over-tero-rs` | section | — | Tero (documentation / corpus context) — now dynamic over tero-rs | `AGENTS.md:3` | — | Use Tero (Python presenter over tero-rs binary) for cited lookups. The surface (tools, args, inputSchemas with Rust type hints, categories: introspection/query… |
| `agents--prefer` | section | — | Prefer | `AGENTS.md:13` | — | 1. textsearch / querybyid / querybykind via the tero MCP server (when registered in Grok). |
| `agents--subagents-and-multi-repo-excavation-required-when-tero-is-available` | section | — | Subagents and multi-repo excavation (required when Tero is available) | `AGENTS.md:19` | — | Sibling-tool investigations, readiness audits, and design waves are harder if agents only ls/grep checkouts. Every agent that excavates (orchestrator and leaf… |
| `agents--tero-excavation-do-this-before-deep-filesystem-greps` | section | — | Tero excavation (do this before deep filesystem greps) | `AGENTS.md:33` | — | You have access to the tero MCP server (tools tero). Use it to excavate project |
| `agents--if-this-session-has-no-tero-tools` | section | — | If this session has no `tero__*` tools | `AGENTS.md:52` | — | Sessions only pick up MCP servers registered before launch (or after /mcps → r). Quick path: |
| `agents--1-one-time-sibling-package-index-adjust-gitparent` | other | — | 1) One-time: sibling package + index (adjust GIT_PARENT) | `AGENTS.md:57` | — | export GITPARENT="${GITPARENT:-$HOME/git}" |
| `agents--2-register-user-scope-.grok-config.toml` | other | — | 2) Register (user scope → ~/.grok/config.toml) | `AGENTS.md:62` | — | grok mcp add tero \ |
| `agents--3-verify-then-new-session-or-mcps-r-if-already-inside-tui` | other | — | 3) Verify, then new session (or /mcps → r if already inside TUI) | `AGENTS.md:69` | — | grok mcp doctor tero   # handshake OK, 9 tools |
| `agents--grok-mcp-when-available` | section | — | Grok MCP (when available) | `AGENTS.md:75` | — | - Server name: tero → tools namespaced tero… |
| `agents--this-repos-agent-cli-tui` | section | — | This repo’s agent CLI/TUI | `AGENTS.md:100` | — | Independent of Grok MCP registration: |
| `agents--latest-state-w2-facade-integration-2026-07-09` | section | — | Latest State (W2 Facade + Integration, 2026-07-09) | `AGENTS.md:112` | — | - W2 CommonMemory facade implementation: CommonMemoryAdapter + AgentDomain M1 (full Py mirror of memory-gate-rs M1 domains with prefix parsing: GENERAL, TERO,… |
| `agents--post-c0-fix-for-pr12-2026-07-09-appended` | section | — | Post C0 Fix for PR#12 (2026-07-09, appended) | `AGENTS.md:129` | — | - CRITICAL blocker resolved: in CommonMemoryAdapter.query (schemas.py) tero backend error returned as explicit StructuredResponse.refusal (per facade contract… |
| `agents--pr12-reviewmerge-agent-2026-07-09-appended` | section | — | PR#12 Review+Merge Agent (2026-07-09 appended) | `AGENTS.md:142` | — | - Tero-first (MCP + script): teroidentify + textsearch "cabal W2 facade" "C0 PR#12" "dev-docs wsfull-wave-2026-07-09-compact" (hits: workspacecabalteroreadines… |
| `agents--honest-docs-closure-chore-honest-docs-post-w2-2026-07-09-appended` | section | — | Honest docs closure (chore/honest-docs-post-w2, 2026-07-09 appended) | `AGENTS.md:161` | — | - Tero-first (MCP identify + textsearch "W2 Facade"\|"C0"\|"POC"\|"wsfull-wave" + cite reads of dev-docs/waves/ + WORKSPACE... before greps/edits). Read cited + P… |
| `agents--poc-6-iteration-documented-single-shot-chore-poc6-iteration-honesty-appended-2026-07-09` | section | POC-6 | POC-6 iteration documented single-shot (chore/poc6-iteration-honesty appended 2026-07-09) | `AGENTS.md:169` | — | - Tero-first (required): /root/git/scripts/tero.sh cabal-devmelopner textsearch "POC-6\|iteration" (refusal, 156 rows, no prior match); re-ran for "POC","plan",… |
| `agents--mvp-1-minimal-tools-start-chore-mvp1-tools-start-appended-2026-07-09` | section | MVP-1 | MVP-1 minimal tools start (chore/mvp1-tools-start appended 2026-07-09) | `AGENTS.md:181` | — | - Task: start MVP-1 per plan.md p2 cabal-poc-mvp (parallel to w2): B1 tool host v0 (readfile/listdir/runcommand allowlisted + TOOL events), B2 loop (model prop… |
| `phase` | section | — | cabal-devmelopner — Development Phases | `PHASE.md:1` | — | This document tracks the phased development of cabal-devmelopner. |
| `phase--poc-phase-current` | section | — | PoC Phase (Current) | `PHASE.md:11` | — | Goal: Validate core architecture and get a working, extensible agent. |
| `phase--deliverables` | section | — | Deliverables | `PHASE.md:15` | — | - [x] Project skeleton + installable CLI |
| `phase--recent-wave-updates-w2-facade-integration-2026-07-09` | section | — | Recent Wave Updates (W2 Facade + Integration, 2026-07-09) | `PHASE.md:22` | — | As part of wsfull PR process: |
| `phase--exit-criteria` | section | — | Exit Criteria | `PHASE.md:44` | — | PoC not exited until testing/stabilization (POC-7) are honest; iteration/feedback (POC-6) is now documented as single-shot (honest deferral to MVP/tools per pl… |
| `phase--mvp-phase` | section | — | MVP Phase | `PHASE.md:57` | — | Goal: Make cabal-devmelopner a practical daily co-dev tool. |
| `phase--key-features` | section | — | Key Features | `PHASE.md:61` | — | - Full-featured TUI (status, progress, logs, task management) |
| `phase--exit-criteria-2` | section | — | Exit Criteria | `PHASE.md:72` | — | - Comfortable to use for real development work. |
| `phase--production-phase` | section | — | Production Phase | `PHASE.md:80` | — | Goal: Robust, scalable, multi-agent development system. |
| `phase--key-features-2` | section | — | Key Features | `PHASE.md:84` | — | - Multi-provider support (xAI, Claude, others) |
| `phase--exit-criteria-3` | section | — | Exit Criteria | `PHASE.md:97` | — | - Can reliably run long development sessions with minimal human intervention. |
| `phase--notes` | section | — | Notes | `PHASE.md:105` | — | - All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture. |
| `phase--mvp-1-tools-start-appended-2026-07-09-chore-mvp1-tools-start-per-plan.md-p2` | section | MVP-1 | MVP-1 tools start (appended 2026-07-09, chore/mvp1-tools-start per plan.md p2) | `PHASE.md:111` | — | - Started B1 (tool host v0 in core/tools.py: read/list/run allowlisted, emit TOOL) + B2 (agent loop detect/execute/feedback re-prompt). |
| `phase--appended-w2-c0-fix-for-pr12-2026-07-09` | section | — | Appended: W2 + C0 fix for PR#12 (2026-07-09) | `PHASE.md:121` | — | - W2 facade + AgentDomain + StructuredResponse wired + C0 error emit fixed (agent.py + test green). |
| `phase--honest-poc-status-alignment-chore-honest-docs-post-w2-2026-07-09` | section | — | Honest PoC status alignment (chore/honest-docs-post-w2, 2026-07-09) | `PHASE.md:127` | — | - Updated lagging PoC bullets + exit criteria for TUI (now entrypoint + Task met post A1-A3) and Tero error handling (C0/POC-4 addressed, facade path). |
| `phase--poc-6-iteration-honesty-chore-poc6-iteration-honesty-per-plan.md-p2` | section | POC-6 | POC-6 iteration honesty (chore/poc6-iteration-honesty, per plan.md p2) | `PHASE.md:134` | — | - Decision: Document POC-6 as single-shot (honest); defer full multi-iteration feedback + verification loop to MVP/tools (Wave B: B2/B4 etc). Matches code real… |
| `readme` | other | — | cabal-devmelopner | `README.md:1` | — | cabal-devmelopner is a repo-agnostic development agent designed for long-running, high-quality coding assistance. |
| `readme--features-poc` | section | — | Features (PoC) | `README.md:7` | — | - Uses Grok via the raw xAI API |
| `readme--setup-recommended-uv` | section | — | Setup (Recommended: UV) | `README.md:17` | — | This project uses uv for Python version management, dependency resolution, and running. |
| `readme--one-command-setup-ubuntu-wsl-macos-linux` | section | — | One-command setup (Ubuntu / WSL / macOS / Linux) | `README.md:21` | — | git clone https://github.com/tzervas/cabal-devmelopner.git |
| `readme--manual-setup` | section | — | Manual setup | `README.md:29` | — | curl -LsSf https://astral.sh/uv/install.sh \| sh |
| `readme--1.-install-uv-if-you-dont-have-it` | other | — | 1. Install uv if you don't have it | `README.md:32` | — | curl -LsSf https://astral.sh/uv/install.sh \| sh |
| `readme--2.-clone-and-enter-the-repo` | other | — | 2. Clone and enter the repo | `README.md:35` | — | cd cabal-devmelopner |
| `readme--3.-sync-environment` | other | — | 3. Sync environment | `README.md:38` | — | uv sync --all-extras |
| `readme--tero-optional-for-corpus-context` | section | — | Tero (optional, for corpus context) | `README.md:42` | — | Tero is opt-in. Defaults expect sibling checkouts next to this repo: |
| `readme--running` | section | — | Running | `README.md:60` | — | uv run cabal-devmelopner "Refactor using memory-gate + tero" --use-tero --local-model qwen2.5-coder:7b |
| `readme--local-self-hosted-default-gpu-on-5080-full-pipeline-with-tero-w2-schemas` | other | — | Local self-hosted (default, GPU on 5080; full pipeline with tero + W2 schemas) | `README.md:63` | — | uv run cabal-devmelopner "Refactor using memory-gate + tero" --use-tero --local-model qwen2.5-coder:7b |
| `readme--frontier-explicit` | other | — | Frontier explicit | `README.md:66` | — | export XAIAPIKEY=... |
| `readme--tui-entrypoint-fixed-pr12-a1-poc-surface` | other | — | TUI (entrypoint fixed PR#12 A1; PoC surface) | `README.md:70` | — | uv run cabal-devmelopner-tui |
| `readme--tui-with-tero` | other | — | TUI with Tero | `README.md:73` | — | USETERO=true uv run cabal-devmelopner-tui |
| `readme--architecture-notes` | section | — | Architecture Notes | `README.md:82` | — | - EventBus: Central communication mechanism (producer/consumer model) |
| `readme--documentation` | section | — | Documentation | `README.md:89` | — | — |
| `readme--development-phases` | section | — | Development Phases | `README.md:101` | — | See [PHASE.md](PHASE.md) for the roadmap. PoC is not exited until P0 TUI entrypoint and basic stabilization items are addressed. |
| `readme--license` | section | — | License | `README.md:105` | — | MIT |
| `readme--latest-wave-w2-facade-pr-process` | section | — | Latest Wave (W2 + Facade, PR process) | `README.md:109` | — | W2 CommonMemoryAdapter + AgentDomain (M1) fully wired in core/schemas.py + agent.py (runstructured uses facade for tero domain queries, StructuredResponse + ci… |
| `readme--post-fix-append-c0-resolved-2026-07-09` | section | — | Post-fix append (C0 resolved) 2026-07-09 | `README.md:119` | — | - W2 CommonMemory facade (CommonMemoryAdapter + AgentDomain M1 from memory-gate-rs) implemented in core/schemas.py + wired into agent (runstructured uses facad… |
| `intentandgapanalysis` | section | — | Intent and Gap Analysis | `docs/INTENT_AND_GAP_ANALYSIS.md:1` | Living document — update when PoC exit criteria or architecture change. | Baseline: dev (includes Tero docs/client commit 32d30d3) |
| `intentandgapanalysis--1.-stated-intent` | section | — | 1. Stated intent | `docs/INTENT_AND_GAP_ANALYSIS.md:11` | — | Core principles: repo-agnostic · extensible communications · strong Tero integration · clean architecture. |
| `intentandgapanalysis--recent-updates-w2-facade-as-of-pr-process-2026-07-09` | section | — | Recent Updates (W2 + Facade, as of PR process 2026-07-09) | `docs/INTENT_AND_GAP_ANALYSIS.md:22` | — | - W2 schemas + CommonMemory facade implementation landed in core/schemas.py: StructuredResponse/Prompt (W2), Citation, MemoryContext, AgentDomain (M1 mirror fr… |
| `intentandgapanalysis--2.-current-implementation-snapshot` | section | — | 2. Current implementation (snapshot) | `docs/INTENT_AND_GAP_ANALYSIS.md:37` | — | Approximate application size: ~550+ LOC under src/cabaldevmelopner/. |
| `intentandgapanalysis--architecture-as-implemented` | section | — | Architecture (as implemented) | `docs/INTENT_AND_GAP_ANALYSIS.md:57` | — | CLI / TUI  →  SimpleAgent  →  Provider.complete(prompt) |
| `intentandgapanalysis--3.-poc-checklist-intent-vs-reality` | section | — | 3. PoC checklist: intent vs reality | `docs/INTENT_AND_GAP_ANALYSIS.md:70` | — | — |
| `intentandgapanalysis--poc-exit-criteria` | section | — | PoC exit criteria | `docs/INTENT_AND_GAP_ANALYSIS.md:84` | — | — |
| `intentandgapanalysis--4.-critical-gaps` | section | — | 4. Critical gaps | `docs/INTENT_AND_GAP_ANALYSIS.md:94` | — | Intent: coding assistance that acts on repositories. |
| `intentandgapanalysis--4.1-not-a-development-agent-yet` | section | — | 4.1 Not a development agent yet | `docs/INTENT_AND_GAP_ANALYSIS.md:96` | — | Intent: coding assistance that acts on repositories. |
| `intentandgapanalysis--4.2-tui-entrypoint-p0-addressed-pr12` | section | — | 4.2 TUI entrypoint (P0 — addressed PR#12) | `docs/INTENT_AND_GAP_ANALYSIS.md:106` | — | Entrypoint now present (def main() + main guard in app.py; console script wired). TUI uses real Task dataclass (POC-3). Error events wired (A3). |
| `intentandgapanalysis--4.3-tero-improved-but-incomplete` | section | — | 4.3 Tero: improved but incomplete | `docs/INTENT_AND_GAP_ANALYSIS.md:112` | — | Landed improvements (dev): sibling defaults, env overrides, token auth, MCP content envelope unwrap, items-based agent formatting, docs/TERO.md. |
| `intentandgapanalysis--4.4-agent-loop-does-not-iterate` | section | — | 4.4 Agent loop does not iterate | `docs/INTENT_AND_GAP_ANALYSIS.md:126` | — | if iteration == 1: |
| `intentandgapanalysis--4.5-empty-runtime-dependencies` | section | — | 4.5 Empty runtime dependencies | `docs/INTENT_AND_GAP_ANALYSIS.md:136` | — | dependencies = [] |
| `intentandgapanalysis--4.6-tui-bypasses-task-type` | section | — | 4.6 TUI bypasses `Task` type | `docs/INTENT_AND_GAP_ANALYSIS.md:144` | — | Duck-typed type("Task", (), {...})() instead of Task dataclass. |
| `intentandgapanalysis--4.7-status-drift-pre-updates` | section | — | 4.7 Status drift (pre updates) | `docs/INTENT_AND_GAP_ANALYSIS.md:148` | — | Prior docs lagged post-code (e.g. "broken" after A1-A3 in PR#12). This + parallel edits in PHASE/ROADMAP/OPENISSUES close the honesty gap (chore/honest-docs-po… |
| `intentandgapanalysis--5.-secondary-structural-gaps` | section | — | 5. Secondary / structural gaps | `docs/INTENT_AND_GAP_ANALYSIS.md:154` | — | — |
| `intentandgapanalysis--6.-what-is-solid-keep` | section | — | 6. What is solid (keep) | `docs/INTENT_AND_GAP_ANALYSIS.md:170` | — | - Clear phase model (PoC → MVP → Production) |
| `intentandgapanalysis--7.-gap-map-by-phase` | section | — | 7. Gap map by phase | `docs/INTENT_AND_GAP_ANALYSIS.md:183` | — | INTENT                          CURRENT STATE |
| `intentandgapanalysis--8.-recommended-priority-close-poc-honestly` | section | — | 8. Recommended priority (close PoC honestly) | `docs/INTENT_AND_GAP_ANALYSIS.md:205` | — | 1. POC-6 (documented) Iteration/feedback documented as single-shot (plan.md p2 decision); early-return on iter=1 is now honest (defer full to MVP/tools). PHASE… |
| `intentandgapanalysis--9.-bottom-line` | section | — | 9. Bottom line | `docs/INTENT_AND_GAP_ANALYSIS.md:218` | — | Intent: long-running, repo-agnostic development agent with event-driven UIs and strong Tero context. |
| `intentandgapanalysis--appended-post-w2-facade-c0-2026-07-09-pr12-process` | section | — | Appended post-W2 facade + C0 (2026-07-09, PR#12 process) | `docs/INTENT_AND_GAP_ANALYSIS.md:227` | — | - W2 CommonMemory facade (schemas + agent wiring for StructuredResponse + domain queries via tero) closes integration gap for workspace memory. |
| `intentandgapanalysis--honest-status-alignment-chore-honest-docs-post-w2-2026-07-09` | section | — | Honest status alignment (chore/honest-docs-post-w2, 2026-07-09) | `docs/INTENT_AND_GAP_ANALYSIS.md:233` | — | - Fixed lagging text in PoC snapshot/checklist/gaps/priority/bottom-line (TUI entrypoint/POC-1/3, Tero C0/POC-4 now accurate per merged code; iteration kept pa… |
| `intentandgapanalysis--poc-6-single-shot-documented-chore-poc6-iteration-honesty-append-only` | section | POC-6 | POC-6 single-shot documented (chore/poc6-iteration-honesty, append-only) | `docs/INTENT_AND_GAP_ANALYSIS.md:239` | — | - Updated recommended priority, bottom-line reality, PoC gaps note: POC-6 closed as "document or implement" via honest documentation of single-shot. |
| `localchecks` | section | — | Local checks (CI parity) | `docs/LOCAL_CHECKS.md:1` | — | GitHub Actions workflows in this repo are manual only (workflowdispatch). |
| `localchecks--run-everything-the-remote-job-would-run` | section | — | Run everything the remote job would run | `docs/LOCAL_CHECKS.md:6` | — | ./scripts/check.sh |
| `localchecks--tero-index` | section | — | Tero index | `docs/LOCAL_CHECKS.md:19` | — | python3 ../tero-mcp/scripts/generateliteindex.py --root "$(pwd)" |
| `localchecks--from-a-checkout-that-can-see-the-generator-sibling-tero-mcp-recommended` | other | — | from a checkout that can see the generator (sibling tero-mcp recommended): | `docs/LOCAL_CHECKS.md:22` | — | python3 ../tero-mcp/scripts/generateliteindex.py --root "$(pwd)" |
| `localchecks--or` | other | — | or: | `docs/LOCAL_CHECKS.md:24` | — | python3 scripts/generateteroindex.sh   # if present as a thin wrapper |
| `localchecks--remote-optional` | section | — | Remote (optional) | `docs/LOCAL_CHECKS.md:30` | — | In GitHub: Actions → CI → Run workflow. |
| `localtooling` | section | — | Local sibling tooling (MCP / packages) | `docs/LOCAL_TOOLING.md:1` | Living notes (2026-07-08) | Status: Living notes (2026-07-08) |
| `localtooling--inventory-typical-parent-dir` | section | — | Inventory (typical parent dir) | `docs/LOCAL_TOOLING.md:11` | — | — |
| `localtooling--context-mcp-not-legitimate-rag-yet-and-must-become-efficient-legitimate-rag` | section | — | context-mcp: not legitimate RAG yet — and **must become** efficient legitimate RAG | `docs/LOCAL_TOOLING.md:26` | — | Product need (maintainer): context-mcp requires efficient, legitimate RAG — not pseudo-similarity theater. That is an upstream requirement on the context-mcp r… |
| `localtooling--embeddings-gap` | section | — | Embeddings (gap) | `docs/LOCAL_TOOLING.md:33` | — | - Retrieval “semantic” path in src/rag.rs uses texttopseudoembedding: word-hash + sin features into a 64-d vector, then cosine. |
| `localtooling--storage-gap` | section | — | Storage (gap) | `docs/LOCAL_TOOLING.md:40` | — | So today: structured session store + filters/tags/temporal scores + optional disk, with a placeholder similarity channel. Useful agent scratch memory, not legi… |
| `localtooling--definition-of-efficient-legitimate-rag-exit-for-this-gap` | section | — | Definition of “efficient legitimate RAG” (exit for this gap) | `docs/LOCAL_TOOLING.md:50` | — | Upstream context-mcp is RAG-ready only when all of the following hold: |
| `localtooling--split-of-roles-do-not-collapse` | section | — | Split of roles (do not collapse) | `docs/LOCAL_TOOLING.md:63` | — | Cabal may use both: Tero for project truth, context-mcp for runtime/session RAG after the exit criteria above. |
| `localtooling--cabal-integration-rules` | section | — | Cabal integration rules | `docs/LOCAL_TOOLING.md:74` | — | 1. Wave B: default session history = JSONL (B8). Do not depend on context-mcp for “RAG quality.” |
| `localtooling--readiness-for-cabal-context-mcp-only` | section | — | Readiness for cabal (context-mcp only) | `docs/LOCAL_TOOLING.md:81` | — | Suggested issue themes (file on tzervas/context-mcp): |
| `localtooling--upstream-work-context-mcp-repo-track-there` | section | — | Upstream work (context-mcp repo — track there) | `docs/LOCAL_TOOLING.md:90` | — | Suggested issue themes (file on tzervas/context-mcp): |
| `localtooling--other-siblings-one-liners` | section | — | Other siblings (one-liners) | `docs/LOCAL_TOOLING.md:105` | — | Branch/in-flight detail from the 2026-07-08 audit lives in session notes (/tmp/investigate-.md); re-run with Tero-first leaf prompts when refreshing. |
| `localtooling--related` | section | — | Related | `docs/LOCAL_TOOLING.md:119` | — | - [ROADMAP.md](ROADMAP.md) — waves and PR plan |
| `localtooling--per-repo-tero-indices` | section | — | Per-repo Tero indices | `docs/LOCAL_TOOLING.md:126` | — | Each sibling MCP repo (and this one) commits docs/tero-index/ for local tero-mcp-lite. Regenerate with python3 ../tero-mcp/scripts/generateliteindex.py --root… |
| `localtooling--local-ci-parity` | section | — | Local CI parity | `docs/LOCAL_TOOLING.md:130` | — | ./scripts/check.sh |
| `openissues` | section | — | Open issues backlog (from intent / gap analysis) | `docs/OPEN_ISSUES.md:1` | — | Derived from [INTENTANDGAPANALYSIS.md](INTENTANDGAPANALYSIS.md). Execution order, waves, and PR DAG: [ROADMAP.md](ROADMAP.md). Use this file as a checklist for… |
| `openissues--p0-fix-before-claiming-a-working-tui` | section | — | P0 — Fix before claiming a working TUI | `docs/OPEN_ISSUES.md:11` | — | — |
| `openissues--p1-poc-exit-criteria` | section | — | P1 — PoC exit criteria | `docs/OPEN_ISSUES.md:21` | — | — |
| `openissues--p2-toward-a-useful-development-agent-mvp` | section | — | P2 — Toward a useful development agent / MVP | `docs/OPEN_ISSUES.md:34` | — | — |
| `openissues--p3-production-oriented-track-only` | section | — | P3 — Production-oriented (track only) | `docs/OPEN_ISSUES.md:48` | — | — |
| `openissues--suggested-github-issue-titles` | section | — | Suggested GitHub issue titles | `docs/OPEN_ISSUES.md:61` | — | 1. [P0] Fix cabal-devmelopner-tui entrypoint (missing main) |
| `openissues--out-of-scope-for-the-docs-pr-that-added-this-file` | section | — | Out of scope for the docs PR that added this file | `docs/OPEN_ISSUES.md:74` | — | - Implementing the fixes above |
| `openissues--mvp-1-minimal-tools-started-chore-mvp1-tools-start-appended-2026-07-09` | section | MVP-1 | MVP-1 minimal tools started (chore/mvp1-tools-start appended 2026-07-09) | `docs/OPEN_ISSUES.md:79` | — | - Per plan.md p2 (cabal-poc-mvp): B1 tool host v0 (read/list/run + TOOL via EventBus) + B2 loop (model propose/execute/re-prompt) + tero/W2 integrate. |
| `openissues--status-alignment-post-w2-c0-pr12-appended-2026-07-09-chore-honest-docs-post-w2` | section | — | Status alignment post W2/C0 + PR#12 (appended 2026-07-09, chore/honest-docs-post-w2) | `docs/OPEN_ISSUES.md:88` | — | - POC-1 (TUI entrypoint) + POC-3 (real Task): addressed by A1/A2 in PR#12 cab/a1-a3 (now cabal-devmelopner-tui has main(); TUI imports/uses core.types.Task). |
| `openissues--poc-6-documented-as-single-shot-chore-poc6-iteration-honesty-appended` | section | POC-6 | POC-6 documented as single-shot (chore/poc6-iteration-honesty appended) | `docs/OPEN_ISSUES.md:97` | — | - Per plan.md (cabal section priority 2, "cabal-poc-mvp POC-6"): decide/document as single-shot (honest, defer full feedback to MVP/tools). Matches agent.py re… |
| `roadmap` | note | — | cabal-devmelopner — Product Roadmap | `docs/ROADMAP.md:1` | Plan (2026-07-08) | Status: Plan (2026-07-08) |
| `roadmap--1.-north-star` | section | — | 1. North star | `docs/ROADMAP.md:11` | — | cabal-devmelopner is a repo-agnostic development agent: long-running, event-driven, multi-surface (CLI / TUI / future Discord), with strong Tero integration fo… |
| `roadmap--2.-current-position-summary` | section | — | 2. Current position (summary) | `docs/ROADMAP.md:32` | — | PoC exit requires honest tests/stabilization (POC-7); iteration (POC-6) now documented single-shot (honest, per plan.md p2 deferral to MVP/tools); TUI launch (… |
| `roadmap--3.-architecture-target-incremental` | section | — | 3. Architecture target (incremental) | `docs/ROADMAP.md:49` | — | ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ |
| `roadmap--4.-waves` | section | — | 4. Waves | `docs/ROADMAP.md:84` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-a-poc-close-out-make-claims-true` | section | — | Wave A — PoC close-out (make claims true) | `docs/ROADMAP.md:86` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-b-minimum-useful-agent-mvp-core` | section | — | Wave B — Minimum useful agent (MVP core) | `docs/ROADMAP.md:107` | — | Goal: Agent can act on a repo with Tero-assisted context and a real loop. |
| `roadmap--mvp-1-tools-start-chore-mvp1-tools-start-2026-07-09-appended` | section | MVP-1 | MVP-1 tools start (chore/mvp1-tools-start, 2026-07-09 appended) | `docs/ROADMAP.md:129` | — | - B1: core/tools.py (ToolHost + readfile/listdir/runcommand allowlisted + parse + events TOOLCALL/RESULT). |
| `roadmap--wave-c-daily-co-dev-polish-mvp-complete` | section | — | Wave C — Daily co-dev polish (MVP complete) | `docs/ROADMAP.md:143` | — | Goal: Comfortable daily driver. |
| `roadmap--wave-d-multi-agent-production-shape` | section | — | Wave D — Multi-agent & production shape | `docs/ROADMAP.md:160` | — | Goal: Coordinated agents with safe concurrency; security load-bearing. |
| `roadmap--wave-updates-w2-facade-cabal-integration-2026-07-09` | section | — | Wave Updates (W2 Facade + Cabal Integration, 2026-07-09) | `docs/ROADMAP.md:177` | — | As part of wsfull PR process and doc/tero updates: |
| `roadmap--5.-dependency-graph-high-level` | section | — | 5. Dependency graph (high level) | `docs/ROADMAP.md:195` | — | Wave A (PoC honest) |
| `roadmap--6.-pr-plan-incremental-reviewable` | section | — | 6. PR Plan (incremental, reviewable) | `docs/ROADMAP.md:214` | — | Each PR should be independently mergeable to dev. Suggested titles match GitHub issues where they exist. |
| `roadmap--wave-a` | section | — | Wave A | `docs/ROADMAP.md:218` | — | — |
| `roadmap--wave-b` | section | — | Wave B | `docs/ROADMAP.md:230` | — | — |
| `roadmap--wave-c` | section | — | Wave C | `docs/ROADMAP.md:243` | — | — |
| `roadmap--wave-d` | section | — | Wave D | `docs/ROADMAP.md:252` | — | — |
| `roadmap--7.-key-decisions` | section | — | 7. Key decisions | `docs/ROADMAP.md:264` | — | — |
| `roadmap--8.-open-questions-need-maintainer-input` | section | — | 8. Open questions (need maintainer input) | `docs/ROADMAP.md:279` | — | 1. Default tool allowlist — shell unrestricted vs allowlist-only from day one? (Recommend allowlist-only.) |
| `roadmap--9.-suggested-near-term-execution-order-next-2-weeks` | section | — | 9. Suggested near-term execution order (next 2 weeks) | `docs/ROADMAP.md:289` | — | 1. Land docs PR #1 (intent/gap + cold-start) if not merged. |
| `roadmap--10.-success-metrics-lightweight` | section | — | 10. Success metrics (lightweight) | `docs/ROADMAP.md:300` | — | — |
| `roadmap--11.-references-tero-cited` | section | — | 11. References (Tero-cited) | `docs/ROADMAP.md:310` | — | Local product docs: PHASE, INTENTANDGAPANALYSIS, OPENISSUES, TERO. |
| `roadmap--appended-pr12-w2-facade-c0-resolution-2026-07-09` | section | — | Appended: PR#12 W2 facade + C0 resolution (2026-07-09) | `docs/ROADMAP.md:324` | — | - Integrated W2 schemas (Structured, Citation, MemoryContext) + CommonMemoryAdapter + AgentDomain M1 (6+ domains incl. TERO/CONTEXT/MEMORYGATE/LANG). |
| `roadmap--honest-docs-update-chore-honest-docs-post-w2` | section | — | Honest docs update (chore/honest-docs-post-w2) | `docs/ROADMAP.md:331` | — | - Aligned lagging current-position table + Wave A exit text post-PR#12 merges (TUI entrypoint now accurate; POC-1/3/4 closed in code). |
| `roadmap--poc-6-documented-single-shot-chore-poc6-iteration-honesty-per-plan.md-p2` | section | POC-6 | POC-6 documented single-shot (chore/poc6-iteration-honesty per plan.md p2) | `docs/ROADMAP.md:338` | — | - A6 marked documented single-shot; footnote updated; exit/position text revised for honesty (no longer requires POC-6 for PoC exit). |
| `tero` | section | — | Tero-MCP integration | `docs/TERO.md:1` | — | [Tero](https://github.com/tzervas) is a Layer-1 corpus index query surface: cited lookups over docs, decisions, issues, changelog entries, and skills. cabal-de… |
| `tero--what-tero-is-and-is-not` | section | — | What Tero is (and is not) | `docs/TERO.md:9` | — | Treat results as pointers: open the cited path and read the source. Do not treat summaries as ground truth. |
| `tero--expected-sibling-layout` | section | — | Expected sibling layout | `docs/TERO.md:22` | — | Defaults assume a shared parent directory (e.g. ~/git or /root/git): |
| `tero--prerequisites` | section | — | Prerequisites | `docs/TERO.md:37` | — | 1. Python ≥ 3.11 for tero-mcp-lite (this project targets 3.14 via uv). |
| `tero--environment-variables` | section | — | Environment variables | `docs/TERO.md:67` | — | Auto local index: cabal-devmelopner now prefers a docs/tero-index/index.json found by walking up from the current working directory (stops at git root). This m… |
| `tero--using-tero-from-cabal-devmelopner` | section | — | Using Tero from cabal-devmelopner | `docs/TERO.md:80` | — | export XAIAPIKEY="your-xai-key" |
| `tero--cli-opt-in-flag` | section | — | CLI (opt-in flag) | `docs/TERO.md:82` | — | export XAIAPIKEY="your-xai-key" |
| `tero--optional-overrides` | other | — | optional overrides: | `docs/TERO.md:86` | — | uv run cabal-devmelopner "Improve error handling in the compiler frontend" --use-tero |
| `tero--export-teromcpproject-path-to-tero-mcp` | other | — | export TERO_MCP_PROJECT=/path/to/tero-mcp | `docs/TERO.md:87` | — | uv run cabal-devmelopner "Improve error handling in the compiler frontend" --use-tero |
| `tero--export-teroindexpath-path-to-index.json` | other | — | export TERO_INDEX_PATH=/path/to/index.json | `docs/TERO.md:88` | — | uv run cabal-devmelopner "Improve error handling in the compiler frontend" --use-tero |
| `tero--export-terotokenslocal-devrefresh` | other | — | export TERO_TOKENS='local-dev:refresh' | `docs/TERO.md:89` | — | uv run cabal-devmelopner "Improve error handling in the compiler frontend" --use-tero |
| `tero--tui-opt-in-env` | section | — | TUI (opt-in env) | `docs/TERO.md:96` | — | export XAIAPIKEY="your-xai-key" |
| `tero--what-the-agent-does-with-results` | section | — | What the agent does with results | `docs/TERO.md:104` | — | On each iteration (when a client is configured), SimpleAgent: |
| `tero--client-api-in-process` | section | — | Client API (in-process) | `docs/TERO.md:114` | — | from cabaldevmelopner.mcp.teroclient import TeroMCPClient |
| `tero--using-tero-from-grok-mcp` | section | — | Using Tero from Grok (MCP) | `docs/TERO.md:130` | — | There are two ways work hits Tero: |
| `tero--cold-start-session-has-no-tero-server-yet` | section | — | Cold start: session has no `tero` server yet | `docs/TERO.md:141` | — | Use this when searchtool finds no tero tools, grok mcp list omits tero, or a new machine/session never registered the server. |
| `tero--install-uv-if-needed-https-docs.astral.sh-uv` | other | — | Install uv if needed: https://docs.astral.sh/uv/ | `docs/TERO.md:148` | — | curl -LsSf https://astral.sh/uv/install.sh \| sh |
| `tero--shared-parent-example-git-or-root-git` | other | — | Shared parent (example: ~/git or /root/git) | `docs/TERO.md:151` | — | export GITPARENT="${GITPARENT:-$HOME/git}" |
| `tero--clone-tero-mcp-if-missing-use-your-real-remote` | other | — | Clone tero-mcp if missing (use your real remote) | `docs/TERO.md:156` | — | cd tero-mcp && uv sync && cd .. |
| `tero--git-clone-tero-mcp-url-tero-mcp` | other | — | git clone <tero-mcp-url> tero-mcp | `docs/TERO.md:157` | — | cd tero-mcp && uv sync && cd .. |
| `tero--index-mycelium-shaped-example-or-generate-per-tero-mcp-generating-an-index.md` | other | — | Index: Mycelium-shaped example (or generate per tero-mcp/GENERATING-AN-INDEX.md) | `docs/TERO.md:160` | — | test -f "$GITPARENT/mycelium/docs/tero-index/index.json" \ |
| `tero--expect-gitparent-mycelium-docs-tero-index-index.json` | other | — | Expect: $GIT_PARENT/mycelium/docs/tero-index/index.json | `docs/TERO.md:161` | — | test -f "$GITPARENT/mycelium/docs/tero-index/index.json" \ |
| `tero--already-registered-warm-path` | section | — | Already registered (warm path) | `docs/TERO.md:239` | — | If grok mcp doctor tero is healthy but a given session still lacks tools: /mcps → r, or start a new session. Tool names are always namespaced: terotextsearch,… |
| `tero--subagents-must-excavate-with-tero-too` | section | — | Subagents must excavate with Tero too | `docs/TERO.md:243` | — | When an orchestrator spawns leaf agents to investigate sibling tools (MCP servers, security wrappers, wave patterns, etc.): |
| `tero--tools-all-require-token` | section | — | Tools (all require `token`) | `docs/TERO.md:254` | — | — |
| `tero--manual-smoke-test-no-grok` | section | — | Manual smoke test (no Grok) | `docs/TERO.md:282` | — | cd /path/to/tero-mcp |
| `tero--troubleshooting` | section | — | Troubleshooting | `docs/TERO.md:307` | — | — |
| `tero--status-poc` | section | — | Status (PoC) | `docs/TERO.md:323` | — | - [x] TeroMCPClient one-shot stdio client with token + envelope unwrap |
| `tero--w2-facade-updates-2026-07-09-pr-process` | section | — | W2 Facade Updates (2026-07-09 PR process) | `docs/TERO.md:335` | — | Facade (CommonMemoryAdapter) now primary for tero queries in agent: uses AgentDomain (M1 from memory-gate-rs) + returns W2 StructuredResponse (with citations,… |
| `tero--post-c0-fix-2026-07-09` | section | — | Post C0 Fix (2026-07-09) | `docs/TERO.md:341` | — | - After facade wiring, tero error path now guarantees ERROR event emission in agent (C0 never-silent) when facade returns refusal. |
| `readme-2` | other | — | Tero index (Layer 1) | `docs/tero-index/README.md:1` | — | Machine + human citation index for this repository. |
| `readme--regenerate` | section | — | Regenerate | `docs/tero-index/README.md:13` | — | python3 /path/to/tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--or-if-tero-mcp-is-a-sibling` | other | — | or if tero-mcp is a sibling: | `docs/tero-index/README.md:17` | — | python3 ../tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--serve-locally` | section | — | Serve locally | `docs/tero-index/README.md:21` | — | export TEROTOKENS=local-dev:refresh |

