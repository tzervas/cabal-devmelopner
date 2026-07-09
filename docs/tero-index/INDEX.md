# cabal-devmelopner — Tero Index (Layer 1)

> **Honesty:** Empirical/Declared — lite heading/line heuristic over markdown in cabal-devmelopner via tero-mcp/scripts/generate_lite_index.py; source files are ground truth. Generated 2026-07-09.
> Use this index to find where to Read, not as authoritative ground truth.

- **Items:** 138
- **Flagged:** 0
- **item_tag:** `Empirical/Declared`
- **Machine index:** [`index.json`](./index.json)
- **Manifest:** [`MANIFEST.toml`](./MANIFEST.toml)

## doc (138 entries)

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
| `phase` | section | — | cabal-devmelopner — Development Phases | `PHASE.md:1` | — | This document tracks the phased development of cabal-devmelopner. |
| `phase--poc-phase-current` | section | — | PoC Phase (Current) | `PHASE.md:11` | — | Goal: Validate core architecture and get a working, extensible agent. |
| `phase--deliverables` | section | — | Deliverables | `PHASE.md:15` | — | - [x] Project skeleton + installable CLI |
| `phase--exit-criteria` | section | — | Exit Criteria | `PHASE.md:29` | — | PoC not exited until P0 entrypoint is fixed and testing/stabilization is honest about remaining partials. |
| `phase--mvp-phase` | section | — | MVP Phase | `PHASE.md:42` | — | Goal: Make cabal-devmelopner a practical daily co-dev tool. |
| `phase--key-features` | section | — | Key Features | `PHASE.md:46` | — | - Full-featured TUI (status, progress, logs, task management) |
| `phase--exit-criteria-2` | section | — | Exit Criteria | `PHASE.md:57` | — | - Comfortable to use for real development work. |
| `phase--production-phase` | section | — | Production Phase | `PHASE.md:65` | — | Goal: Robust, scalable, multi-agent development system. |
| `phase--key-features-2` | section | — | Key Features | `PHASE.md:69` | — | - Multi-provider support (xAI, Claude, others) |
| `phase--exit-criteria-3` | section | — | Exit Criteria | `PHASE.md:82` | — | - Can reliably run long development sessions with minimal human intervention. |
| `phase--notes` | section | — | Notes | `PHASE.md:90` | — | - All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture. |
| `readme` | other | — | cabal-devmelopner | `README.md:1` | — | cabal-devmelopner is a repo-agnostic development agent designed for long-running, high-quality coding assistance. |
| `readme--features-poc` | section | — | Features (PoC) | `README.md:7` | — | - Uses Grok via the raw xAI API |
| `readme--setup-recommended-uv` | section | — | Setup (Recommended: UV) | `README.md:17` | — | This project uses uv for Python version management, dependency resolution, and running. |
| `readme--one-command-setup-ubuntu-wsl-macos-linux` | section | — | One-command setup (Ubuntu / WSL / macOS / Linux) | `README.md:21` | — | git clone https://github.com/tzervas/cabal-devmelopner.git |
| `readme--manual-setup` | section | — | Manual setup | `README.md:29` | — | curl -LsSf https://astral.sh/uv/install.sh \| sh |
| `readme--1.-install-uv-if-you-dont-have-it` | other | — | 1. Install uv if you don't have it | `README.md:32` | — | curl -LsSf https://astral.sh/uv/install.sh \| sh |
| `readme--2.-clone-and-enter-the-repo` | other | — | 2. Clone and enter the repo | `README.md:35` | — | cd cabal-devmelopner |
| `readme--3.-sync-environment` | other | — | 3. Sync environment | `README.md:38` | — | uv sync --all-extras |
| `readme--tero-optional-for-corpus-context` | section | — | Tero (optional, for corpus context) | `README.md:42` | — | Tero is opt-in. Defaults expect sibling checkouts next to this repo: |
| `readme--running` | section | — | Running | `README.md:60` | — | export XAIAPIKEY="your-xai-key" |
| `readme--cli` | other | — | CLI | `README.md:65` | — | uv run cabal-devmelopner "Improve the public API of the compiler frontend" |
| `readme--cli-with-tero-context` | other | — | CLI with Tero context | `README.md:68` | — | uv run cabal-devmelopner "Improve the public API of the compiler frontend" --use-tero |
| `readme--tui-intended-entrypoint-currently-fails-until-poc-1-lands` | other | POC-1 | TUI (intended entrypoint — currently fails until POC-1 lands) | `README.md:71` | — | uv run cabal-devmelopner-tui |
| `readme--tui-with-tero-once-entrypoint-is-fixed` | other | — | TUI with Tero (once entrypoint is fixed) | `README.md:74` | — | USETERO=true uv run cabal-devmelopner-tui |
| `readme--architecture-notes` | section | — | Architecture Notes | `README.md:83` | — | - EventBus: Central communication mechanism (producer/consumer model) |
| `readme--documentation` | section | — | Documentation | `README.md:90` | — | — |
| `readme--development-phases` | section | — | Development Phases | `README.md:102` | — | See [PHASE.md](PHASE.md) for the roadmap. PoC is not exited until P0 TUI entrypoint and basic stabilization items are addressed. |
| `readme--license` | section | — | License | `README.md:106` | — | MIT |
| `intentandgapanalysis` | section | — | Intent and Gap Analysis | `docs/INTENT_AND_GAP_ANALYSIS.md:1` | Living document — update when PoC exit criteria or architecture change. | Baseline: dev (includes Tero docs/client commit 32d30d3) |
| `intentandgapanalysis--1.-stated-intent` | section | — | 1. Stated intent | `docs/INTENT_AND_GAP_ANALYSIS.md:11` | — | Core principles: repo-agnostic · extensible communications · strong Tero integration · clean architecture. |
| `intentandgapanalysis--2.-current-implementation-snapshot` | section | — | 2. Current implementation (snapshot) | `docs/INTENT_AND_GAP_ANALYSIS.md:24` | — | Approximate application size: ~550+ LOC under src/cabaldevmelopner/. |
| `intentandgapanalysis--architecture-as-implemented` | section | — | Architecture (as implemented) | `docs/INTENT_AND_GAP_ANALYSIS.md:44` | — | CLI / TUI  →  SimpleAgent  →  Provider.complete(prompt) |
| `intentandgapanalysis--3.-poc-checklist-intent-vs-reality` | section | — | 3. PoC checklist: intent vs reality | `docs/INTENT_AND_GAP_ANALYSIS.md:57` | — | — |
| `intentandgapanalysis--poc-exit-criteria` | section | — | PoC exit criteria | `docs/INTENT_AND_GAP_ANALYSIS.md:71` | — | — |
| `intentandgapanalysis--4.-critical-gaps` | section | — | 4. Critical gaps | `docs/INTENT_AND_GAP_ANALYSIS.md:81` | — | Intent: coding assistance that acts on repositories. |
| `intentandgapanalysis--4.1-not-a-development-agent-yet` | section | — | 4.1 Not a development agent yet | `docs/INTENT_AND_GAP_ANALYSIS.md:83` | — | Intent: coding assistance that acts on repositories. |
| `intentandgapanalysis--4.2-tui-entrypoint-broken-p0` | section | — | 4.2 TUI entrypoint broken (P0) | `docs/INTENT_AND_GAP_ANALYSIS.md:93` | — | cabal-devmelopner-tui → ImportError: cannot import name 'main' |
| `intentandgapanalysis--4.3-tero-improved-but-incomplete` | section | — | 4.3 Tero: improved but incomplete | `docs/INTENT_AND_GAP_ANALYSIS.md:101` | — | Landed improvements (dev): sibling defaults, env overrides, token auth, MCP content envelope unwrap, items-based agent formatting, docs/TERO.md. |
| `intentandgapanalysis--4.4-agent-loop-does-not-iterate` | section | — | 4.4 Agent loop does not iterate | `docs/INTENT_AND_GAP_ANALYSIS.md:115` | — | if iteration == 1: |
| `intentandgapanalysis--4.5-empty-runtime-dependencies` | section | — | 4.5 Empty runtime dependencies | `docs/INTENT_AND_GAP_ANALYSIS.md:125` | — | dependencies = [] |
| `intentandgapanalysis--4.6-tui-bypasses-task-type` | section | — | 4.6 TUI bypasses `Task` type | `docs/INTENT_AND_GAP_ANALYSIS.md:133` | — | Duck-typed type("Task", (), {...})() instead of Task dataclass. |
| `intentandgapanalysis--4.7-status-drift-pre-this-docs-update` | section | — | 4.7 Status drift (pre this docs update) | `docs/INTENT_AND_GAP_ANALYSIS.md:137` | — | PHASE marked TUI and docs fully done while TUI entrypoint failed and multi-iteration remained nominal. Prefer checkboxes that match [OPENISSUES.md](OPENISSUES.… |
| `intentandgapanalysis--5.-secondary-structural-gaps` | section | — | 5. Secondary / structural gaps | `docs/INTENT_AND_GAP_ANALYSIS.md:143` | — | — |
| `intentandgapanalysis--6.-what-is-solid-keep` | section | — | 6. What is solid (keep) | `docs/INTENT_AND_GAP_ANALYSIS.md:159` | — | - Clear phase model (PoC → MVP → Production) |
| `intentandgapanalysis--7.-gap-map-by-phase` | section | — | 7. Gap map by phase | `docs/INTENT_AND_GAP_ANALYSIS.md:172` | — | INTENT                          CURRENT STATE |
| `intentandgapanalysis--8.-recommended-priority-close-poc-honestly` | section | — | 8. Recommended priority (close PoC honestly) | `docs/INTENT_AND_GAP_ANALYSIS.md:194` | — | 1. POC-1 Fix TUI main entrypoint (+ optional main). |
| `intentandgapanalysis--9.-bottom-line` | section | — | 9. Bottom line | `docs/INTENT_AND_GAP_ANALYSIS.md:208` | — | Intent: long-running, repo-agnostic development agent with event-driven UIs and strong Tero context. |
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
| `roadmap` | note | — | cabal-devmelopner — Product Roadmap | `docs/ROADMAP.md:1` | Plan (2026-07-08) | Status: Plan (2026-07-08) |
| `roadmap--1.-north-star` | section | — | 1. North star | `docs/ROADMAP.md:11` | — | cabal-devmelopner is a repo-agnostic development agent: long-running, event-driven, multi-surface (CLI / TUI / future Discord), with strong Tero integration fo… |
| `roadmap--2.-current-position-summary` | section | — | 2. Current position (summary) | `docs/ROADMAP.md:32` | — | PoC exit requires P0 TUI launch + honest tests/stabilization. MVP exit requires tools + verification + usable TUI/config. Production is multi-agent + security… |
| `roadmap--3.-architecture-target-incremental` | section | — | 3. Architecture target (incremental) | `docs/ROADMAP.md:49` | — | ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ |
| `roadmap--4.-waves` | section | — | 4. Waves | `docs/ROADMAP.md:84` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-a-poc-close-out-make-claims-true` | section | — | Wave A — PoC close-out (make claims true) | `docs/ROADMAP.md:86` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-b-minimum-useful-agent-mvp-core` | section | — | Wave B — Minimum useful agent (MVP core) | `docs/ROADMAP.md:107` | — | Goal: Agent can act on a repo with Tero-assisted context and a real loop. |
| `roadmap--wave-c-daily-co-dev-polish-mvp-complete` | section | — | Wave C — Daily co-dev polish (MVP complete) | `docs/ROADMAP.md:131` | — | Goal: Comfortable daily driver. |
| `roadmap--wave-d-multi-agent-production-shape` | section | — | Wave D — Multi-agent & production shape | `docs/ROADMAP.md:148` | — | Goal: Coordinated agents with safe concurrency; security load-bearing. |
| `roadmap--5.-dependency-graph-high-level` | section | — | 5. Dependency graph (high level) | `docs/ROADMAP.md:167` | — | Wave A (PoC honest) |
| `roadmap--6.-pr-plan-incremental-reviewable` | section | — | 6. PR Plan (incremental, reviewable) | `docs/ROADMAP.md:186` | — | Each PR should be independently mergeable to dev. Suggested titles match GitHub issues where they exist. |
| `roadmap--wave-a` | section | — | Wave A | `docs/ROADMAP.md:190` | — | — |
| `roadmap--wave-b` | section | — | Wave B | `docs/ROADMAP.md:202` | — | — |
| `roadmap--wave-c` | section | — | Wave C | `docs/ROADMAP.md:215` | — | — |
| `roadmap--wave-d` | section | — | Wave D | `docs/ROADMAP.md:224` | — | — |
| `roadmap--7.-key-decisions` | section | — | 7. Key decisions | `docs/ROADMAP.md:236` | — | — |
| `roadmap--8.-open-questions-need-maintainer-input` | section | — | 8. Open questions (need maintainer input) | `docs/ROADMAP.md:251` | — | 1. Default tool allowlist — shell unrestricted vs allowlist-only from day one? (Recommend allowlist-only.) |
| `roadmap--9.-suggested-near-term-execution-order-next-2-weeks` | section | — | 9. Suggested near-term execution order (next 2 weeks) | `docs/ROADMAP.md:261` | — | 1. Land docs PR #1 (intent/gap + cold-start) if not merged. |
| `roadmap--10.-success-metrics-lightweight` | section | — | 10. Success metrics (lightweight) | `docs/ROADMAP.md:272` | — | — |
| `roadmap--11.-references-tero-cited` | section | — | 11. References (Tero-cited) | `docs/ROADMAP.md:282` | — | Local product docs: PHASE, INTENTANDGAPANALYSIS, OPENISSUES, TERO. |
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
| `readme-2` | other | — | Tero index (Layer 1) | `docs/tero-index/README.md:1` | — | Machine + human citation index for this repository. |
| `readme--regenerate` | section | — | Regenerate | `docs/tero-index/README.md:13` | — | python3 /path/to/tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--or-if-tero-mcp-is-a-sibling` | other | — | or if tero-mcp is a sibling: | `docs/tero-index/README.md:17` | — | python3 ../tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--serve-locally` | section | — | Serve locally | `docs/tero-index/README.md:21` | — | export TEROTOKENS=local-dev:refresh |

