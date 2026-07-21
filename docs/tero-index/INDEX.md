# cabal-devmelopner — Tero Index (Layer 1)

> **Honesty:** Empirical/Declared — lite heading/line heuristic over markdown in cabal-devmelopner via tero-mcp/scripts/generate_lite_index.py; source files are ground truth. Generated 2026-07-21.
> Use this index to find where to Read, not as authoritative ground truth.

- **Items:** 275
- **Flagged:** 0
- **item_tag:** `Empirical/Declared`
- **Machine index:** [`index.json`](./index.json)
- **Manifest:** [`MANIFEST.toml`](./MANIFEST.toml)

## doc (263 entries)

| Anchor | Kind | Id | Title | File:Line | Status | Summary |
|---|---|---|---|---|---|---|
| `agents` | section | — | Agent notes — cabal-devmelopner | `AGENTS.md:1` | — | Operator-style rules for solo AI and multi-agent L0/L1 (fractal) waves. |
| `agents--product-alpha-0.1.x` | section | — | Product (alpha 0.1.x) | `AGENTS.md:6` | — | - Role: repo-agnostic development agent (CLI/TUI), leaf executor in swarms |
| `agents--fractal-model-policy-l0-l1` | section | — | Fractal model policy (L0 / L1) | `AGENTS.md:14` | — | - Select via cabal.toml agent.profile or CLI --profile l0\|l1 |
| `agents--local-gates` | section | — | Local gates | `AGENTS.md:25` | — | ./scripts/check.sh |
| `agents--branch-pr-guards` | section | — | Branch / PR guards | `AGENTS.md:35` | — | - Branch from dev; never commit directly to main |
| `agents--tero-documentation-corpus-context-now-dynamic-over-tero-rs` | section | — | Tero (documentation / corpus context) — now dynamic over tero-rs | `AGENTS.md:43` | — | Use Tero (Python presenter over tero-rs binary) for cited lookups. The surface (tools, args, inputSchemas with Rust type hints, categories: introspection/query… |
| `agents--prefer` | section | — | Prefer | `AGENTS.md:53` | — | 1. textsearch / querybyid / querybykind via the tero MCP server (when registered in Grok). |
| `agents--subagents-and-multi-repo-excavation-required-when-tero-is-available` | section | — | Subagents and multi-repo excavation (required when Tero is available) | `AGENTS.md:59` | — | Sibling-tool investigations, readiness audits, and design waves are harder if agents only ls/grep checkouts. Every agent that excavates (orchestrator and leaf… |
| `agents--tero-excavation-do-this-before-deep-filesystem-greps` | section | — | Tero excavation (do this before deep filesystem greps) | `AGENTS.md:73` | — | You have access to the tero MCP server (tools tero). Use it to excavate project |
| `agents--if-this-session-has-no-tero-tools` | section | — | If this session has no `tero__*` tools | `AGENTS.md:92` | — | Sessions only pick up MCP servers registered before launch (or after /mcps → r). Quick path: |
| `agents--1-one-time-sibling-package-index-adjust-gitparent` | other | — | 1) One-time: sibling package + index (adjust GIT_PARENT) | `AGENTS.md:97` | — | export GITPARENT="${GITPARENT:-$HOME/git}" |
| `agents--2-register-user-scope-.grok-config.toml` | other | — | 2) Register (user scope → ~/.grok/config.toml) | `AGENTS.md:102` | — | grok mcp add tero \ |
| `agents--3-verify-then-new-session-or-mcps-r-if-already-inside-tui` | other | — | 3) Verify, then new session (or /mcps → r if already inside TUI) | `AGENTS.md:109` | — | grok mcp doctor tero   # handshake OK, 9 tools |
| `agents--grok-mcp-when-available` | section | — | Grok MCP (when available) | `AGENTS.md:115` | — | - Server name: tero → tools namespaced tero… |
| `agents--this-repos-agent-cli-tui` | section | — | This repo’s agent CLI/TUI | `AGENTS.md:140` | — | Independent of Grok MCP registration: |
| `agents--latest-state-w2-facade-integration-2026-07-09` | section | — | Latest State (W2 Facade + Integration, 2026-07-09) | `AGENTS.md:152` | — | - W2 CommonMemory facade implementation: CommonMemoryAdapter + AgentDomain M1 (full Py mirror of memory-gate-rs M1 domains with prefix parsing: GENERAL, TERO,… |
| `agents--post-c0-fix-for-pr12-2026-07-09-appended` | section | — | Post C0 Fix for PR#12 (2026-07-09, appended) | `AGENTS.md:169` | — | - CRITICAL blocker resolved: in CommonMemoryAdapter.query (schemas.py) tero backend error returned as explicit StructuredResponse.refusal (per facade contract… |
| `agents--pr12-reviewmerge-agent-2026-07-09-appended` | section | — | PR#12 Review+Merge Agent (2026-07-09 appended) | `AGENTS.md:182` | — | - Tero-first (MCP + script): teroidentify + textsearch "cabal W2 facade" "C0 PR#12" "dev-docs wsfull-wave-2026-07-09-compact" (hits: workspacecabalteroreadines… |
| `agents--honest-docs-closure-chore-honest-docs-post-w2-2026-07-09-appended` | section | — | Honest docs closure (chore/honest-docs-post-w2, 2026-07-09 appended) | `AGENTS.md:201` | — | - Tero-first (MCP identify + textsearch "W2 Facade"\|"C0"\|"POC"\|"wsfull-wave" + cite reads of dev-docs/waves/ + WORKSPACE... before greps/edits). Read cited + P… |
| `agents--poc-6-iteration-documented-single-shot-chore-poc6-iteration-honesty-appended-2026-07-09` | section | POC-6 | POC-6 iteration documented single-shot (chore/poc6-iteration-honesty appended 2026-07-09) | `AGENTS.md:209` | — | - Tero-first (required): /root/git/scripts/tero.sh cabal-devmelopner textsearch "POC-6\|iteration" (refusal, 156 rows, no prior match); re-ran for "POC","plan",… |
| `agents--mvp-1-minimal-tools-start-chore-mvp1-tools-start-appended-2026-07-09` | section | MVP-1 | MVP-1 minimal tools start (chore/mvp1-tools-start appended 2026-07-09) | `AGENTS.md:221` | — | - Task: start MVP-1 per plan.md p2 cabal-poc-mvp (parallel to w2): B1 tool host v0 (readfile/listdir/runcommand allowlisted + TOOL events), B2 loop (model prop… |
| `agents--dev-mcp-orch-use-cabal-as-leaf-for-dev-mcp-tasks-chore-orch-wiring-devmcp-appended` | section | — | dev-mcp Orch Use (cabal as leaf for dev-mcp tasks; chore/orch-wiring-devmcp appended) | `AGENTS.md:243` | — | cabal-devmelopner is the leaf consumer/executor for dev-mcp orch tasks: |
| `agents--p28b-production-polish-feat-p28-production-appended-2026-07-16` | section | — | P28b production polish (feat/p28-production appended 2026-07-16) | `AGENTS.md:263` | — | - Bar: plans/fractal/P28AIDEVTOOLINGPRODUCTION.md Wave A cabal-devmelopner |
| `claude` | section | — | cabal-devmelopner — Claude / coding-assistant context | `CLAUDE.md:1` | — | cabal-devmelopner is a repo-agnostic development agent (CLI + TUI) with |
| `claude--overview` | section | — | Overview | `CLAUDE.md:3` | — | cabal-devmelopner is a repo-agnostic development agent (CLI + TUI) with |
| `claude--project-map` | section | — | Project map | `CLAUDE.md:10` | — | src/cabaldevmelopner/ |
| `claude--development-commands` | section | — | Development commands | `CLAUDE.md:32` | — | ./setup.sh                 # one-shot: uv + sync |
| `claude--config-as-code` | section | — | Config-as-code | `CLAUDE.md:45` | — | Copy cabal.example.toml → cabal.toml (optional). Profiles: |
| `claude--coding-standards` | section | — | Coding standards | `CLAUDE.md:58` | — | - Prefer small, reviewable diffs |
| `claude--pr-hygiene` | section | — | PR hygiene | `CLAUDE.md:67` | — | Branch from dev. Never push directly to main. |
| `claude--compose` | section | — | Compose | `CLAUDE.md:76` | — | How this plugs into tz-forge agent-swarm, agent-harness, and |
| `claude--further-reading` | section | — | Further reading | `CLAUDE.md:81` | — | - [README.md](README.md) — 5-minute path |
| `phase` | section | — | cabal-devmelopner — Development Phases | `PHASE.md:1` | — | This document tracks the phased development of cabal-devmelopner. |
| `phase--poc-phase-current` | section | — | PoC Phase (Current) | `PHASE.md:11` | — | Goal: Validate core architecture and get a working, extensible agent. |
| `phase--deliverables` | section | — | Deliverables | `PHASE.md:15` | — | - [x] Project skeleton + installable CLI |
| `phase--recent-wave-updates-w2-facade-integration-2026-07-09` | section | — | Recent Wave Updates (W2 Facade + Integration, 2026-07-09) | `PHASE.md:22` | — | As part of wsfull PR process: |
| `phase--exit-criteria` | section | — | Exit Criteria | `PHASE.md:44` | — | PoC not exited until testing/stabilization (POC-7) are honest; iteration/feedback (POC-6) is now documented as single-shot (honest deferral to MVP/tools per pl… |
| `phase--mvp-phase` | section | — | MVP Phase | `PHASE.md:57` | — | Goal: Make cabal-devmelopner a practical daily co-dev tool. |
| `phase--key-features` | section | — | Key Features | `PHASE.md:61` | — | - Full-featured TUI (status, progress, logs, task management) |
| `phase--exit-criteria-2` | section | — | Exit Criteria | `PHASE.md:73` | — | - Comfortable to use for real development work. |
| `phase--production-phase` | section | — | Production Phase | `PHASE.md:81` | — | Goal: Robust, scalable, multi-agent development system. |
| `phase--key-features-2` | section | — | Key Features | `PHASE.md:85` | — | - Multi-provider support (xAI, Claude, others) |
| `phase--exit-criteria-3` | section | — | Exit Criteria | `PHASE.md:98` | — | - Can reliably run long development sessions with minimal human intervention. |
| `phase--notes` | section | — | Notes | `PHASE.md:106` | — | - All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture. |
| `phase--mvp-1-tools-start-appended-2026-07-09-chore-mvp1-tools-start-per-plan.md-p2` | section | MVP-1 | MVP-1 tools start (appended 2026-07-09, chore/mvp1-tools-start per plan.md p2) | `PHASE.md:112` | — | - Started B1 (tool host v0 in core/tools.py: read/list/run allowlisted, emit TOOL) + B2 (agent loop detect/execute/feedback re-prompt). |
| `phase--appended-w2-c0-fix-for-pr12-2026-07-09` | section | — | Appended: W2 + C0 fix for PR#12 (2026-07-09) | `PHASE.md:122` | — | - W2 facade + AgentDomain + StructuredResponse wired + C0 error emit fixed (agent.py + test green). |
| `phase--honest-poc-status-alignment-chore-honest-docs-post-w2-2026-07-09` | section | — | Honest PoC status alignment (chore/honest-docs-post-w2, 2026-07-09) | `PHASE.md:128` | — | - Updated lagging PoC bullets + exit criteria for TUI (now entrypoint + Task met post A1-A3) and Tero error handling (C0/POC-4 addressed, facade path). |
| `phase--poc-6-iteration-honesty-chore-poc6-iteration-honesty-per-plan.md-p2` | section | POC-6 | POC-6 iteration honesty (chore/poc6-iteration-honesty, per plan.md p2) | `PHASE.md:135` | — | - Decision: Document POC-6 as single-shot (honest); defer full multi-iteration feedback + verification loop to MVP/tools (Wave B: B2/B4 etc). Matches code real… |
| `readme` | other | — | cabal-devmelopner | `README.md:1` | — | <!-- FLEET-BADGES:BEGIN --> |
| `readme--5-minute-path` | section | — | 5-minute path | `README.md:23` | — | git clone https://github.com/tzervas/cabal-devmelopner.git |
| `readme--expected-cabal-devmelopner-0.2.1` | other | — | expected: cabal-devmelopner 0.2.1 | `README.md:31` | — | uv run pytest -q |
| `readme--run-a-task` | section | — | Run a task | `README.md:37` | — | uv run cabal-devmelopner "Summarize the project structure" |
| `readme--local-model-ollama-on-localhost11434` | other | — | Local model (Ollama on localhost:11434) | `README.md:40` | — | uv run cabal-devmelopner "Summarize the project structure" |
| `readme--tools-verify-from-cabal.toml-defaults` | other | — | Tools + verify (from cabal.toml / defaults) | `README.md:43` | — | uv run cabal-devmelopner "Add a docstring to README" --use-tools --use-verify |
| `readme--config-profiles` | other | — | Config profiles | `README.md:46` | — | cp cabal.example.toml cabal.toml |
| `readme--frontier` | other | — | Frontier | `README.md:50` | — | export XAIAPIKEY=... |
| `readme--tui` | other | — | TUI | `README.md:54` | — | uv run cabal-devmelopner-tui |
| `readme--optional-tero-sibling` | section | — | Optional: Tero sibling | `README.md:60` | — | <git-parent>/ |
| `readme--config-as-code` | section | — | Config-as-code | `README.md:76` | — | Precedence: CLI > env > cabal.toml > defaults. |
| `readme--features-0.2.0` | section | — | Features (0.2.0) | `README.md:90` | — | - Local Ollama and xAI providers; optional streaming (--stream) |
| `readme--compose-stack` | section | — | Compose stack | `README.md:104` | — | See [docs/COMPOSE.md](docs/COMPOSE.md) and [docs/TOOLINGSTACKREADINESS.md](docs/TOOLINGSTACKREADINESS.md). |
| `readme--documentation` | section | — | Documentation | `README.md:117` | — | — |
| `readme--development` | section | — | Development | `README.md:129` | — | ./scripts/check.sh --quick |
| `readme--license` | section | — | License | `README.md:138` | — | MIT — see [LICENSE](LICENSE). |
| `readme--release` | section | — | Release | `README.md:142` | — | - Semver: [VERSION](VERSION) / [pyproject.toml](pyproject.toml) / version |
| `compose` | section | — | Compose — cabal-devmelopner in the fleet | `docs/COMPOSE.md:1` | — | How this product plugs into tz-forge, agent-harness, tg-agent-relay, |
| `compose--product-role` | section | — | Product role | `docs/COMPOSE.md:7` | — | [tz-forge](https://github.com/tzervas/tz-forge) project kind agent-swarm |
| `compose--tz-forge-agent-swarm-kind` | section | — | tz-forge: `agent-swarm` kind | `docs/COMPOSE.md:17` | — | [tz-forge](https://github.com/tzervas/tz-forge) project kind agent-swarm |
| `compose--from-a-tz-forge-checkout` | other | — | from a tz-forge checkout | `docs/COMPOSE.md:24` | — | python3 cli/tznew.py agent-swarm my-wave --assistant=fractal-swarm |
| `compose--installs-agents-md-fractal-model-policy-kickoffs-cabal-profile-compose-pointer` | other | — | installs: agents-md-fractal + model-policy + kickoffs + cabal-profile COMPOSE pointer | `docs/COMPOSE.md:26` | — | Mirror module doc: tz-forge/docs/compose/cabal-devmelopner.md. |
| `compose--agent-harness` | section | — | agent-harness | `docs/COMPOSE.md:38` | — | Compose rules |
| `compose--sibling-layout-optional` | other | — | sibling layout (optional) | `docs/COMPOSE.md:54` | — | ../agent-harness/   # uv run agent-harness doctor |
| `compose--tg-agent-relay` | section | — | tg-agent-relay | `docs/COMPOSE.md:59` | — | In scope for cabal consumers |
| `compose--tero-mcp-optional-sibling` | section | — | tero-mcp (optional sibling) | `docs/COMPOSE.md:84` | — | <git-parent>/ |
| `compose--config-as-code-profiles` | section | — | Config-as-code profiles | `docs/COMPOSE.md:101` | — | Example: [cabal.example.toml](../cabal.example.toml). Loader: core/config.py. |
| `compose--5-minute-consumer-path` | section | — | 5-minute consumer path | `docs/COMPOSE.md:110` | — | git clone https://github.com/tzervas/cabal-devmelopner.git |
| `compose--offline-smoke-no-model-call` | other | — | Offline smoke (no model call): | `docs/COMPOSE.md:117` | — | uv run pytest -q |
| `compose--non-goals` | section | — | Non-goals | `docs/COMPOSE.md:124` | — | - Embedding cabal binary into tz-forge templates |
| `fleetstandards` | section | — | Fleet standards (tzervas) | `docs/FLEET_STANDARDS.md:1` | — | Applied from the workstation pack under plans/fleet-standards/pack/. |
| `fleetstandards--workflows` | section | — | Workflows | `docs/FLEET_STANDARDS.md:5` | — | - dev / feature merges: Refs #n only — issues stay open |
| `fleetstandards--issue-close-policy` | section | — | Issue close policy | `docs/FLEET_STANDARDS.md:14` | — | - dev / feature merges: Refs #n only — issues stay open |
| `fleetstandards--badges` | section | — | Badges | `docs/FLEET_STANDARDS.md:20` | — | README badges use GitHub Actions SVG for trunk branch — live status, not static green. |
| `fleetstandards--copilot` | section | — | Copilot | `docs/FLEET_STANDARDS.md:24` | — | Automatic Copilot code reviews are disabled for fleet-managed repos. Do not request Copilot on PRs. |
| `fleetstandards--permissions` | section | — | Permissions | `docs/FLEET_STANDARDS.md:28` | — | Workflows use minimum permissions: blocks (contents read; issues write only for close/reopen jobs). |
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
| `localtooling--embeddings-gap` | section | — | Embeddings (gap) | `docs/LOCAL_TOOLING.md:39` | — | - Retrieval “semantic” path in src/rag.rs uses texttopseudoembedding: word-hash + sin features into a 64-d vector, then cosine. |
| `localtooling--storage-gap` | section | — | Storage (gap) | `docs/LOCAL_TOOLING.md:46` | — | So today: structured session store + filters/tags/temporal scores + optional disk, with a placeholder similarity channel. Useful agent scratch memory, not legi… |
| `localtooling--definition-of-efficient-legitimate-rag-exit-for-this-gap` | section | — | Definition of “efficient legitimate RAG” (exit for this gap) | `docs/LOCAL_TOOLING.md:56` | — | Upstream context-mcp is RAG-ready only when all of the following hold: |
| `localtooling--split-of-roles-do-not-collapse` | section | — | Split of roles (do not collapse) | `docs/LOCAL_TOOLING.md:69` | — | Cabal may use both: Tero for project truth, context-mcp for runtime/session RAG after the exit criteria above. |
| `localtooling--cabal-integration-rules` | section | — | Cabal integration rules | `docs/LOCAL_TOOLING.md:80` | — | 1. Wave B: default session history = JSONL (B8). Do not depend on context-mcp for “RAG quality.” |
| `localtooling--readiness-for-cabal-context-mcp-only` | section | — | Readiness for cabal (context-mcp only) | `docs/LOCAL_TOOLING.md:87` | — | Suggested issue themes (file on tzervas/context-mcp): |
| `localtooling--upstream-work-context-mcp-repo-track-there` | section | — | Upstream work (context-mcp repo — track there) | `docs/LOCAL_TOOLING.md:96` | — | Suggested issue themes (file on tzervas/context-mcp): |
| `localtooling--other-siblings-one-liners` | section | — | Other siblings (one-liners) | `docs/LOCAL_TOOLING.md:111` | — | Branch/in-flight detail from the 2026-07-08 audit lives in session notes (/tmp/investigate-.md); re-run with Tero-first leaf prompts when refreshing. |
| `localtooling--related` | section | — | Related | `docs/LOCAL_TOOLING.md:125` | — | - [ROADMAP.md](ROADMAP.md) — waves and PR plan |
| `localtooling--per-repo-tero-indices` | section | — | Per-repo Tero indices | `docs/LOCAL_TOOLING.md:132` | — | Each sibling MCP repo (and this one) commits docs/tero-index/ for local tero-mcp-lite. Regenerate with python3 ../tero-mcp/scripts/generateliteindex.py --root… |
| `localtooling--local-ci-parity` | section | — | Local CI parity | `docs/LOCAL_TOOLING.md:136` | — | ./scripts/check.sh |
| `openissues` | section | — | Open issues backlog (from intent / gap analysis) | `docs/OPEN_ISSUES.md:1` | — | Derived from [INTENTANDGAPANALYSIS.md](INTENTANDGAPANALYSIS.md). Execution order, waves, and PR DAG: [ROADMAP.md](ROADMAP.md). Use this file as a checklist for… |
| `openissues--p0-fix-before-claiming-a-working-tui` | section | — | P0 — Fix before claiming a working TUI | `docs/OPEN_ISSUES.md:14` | — | — |
| `openissues--p1-poc-exit-criteria` | section | — | P1 — PoC exit criteria | `docs/OPEN_ISSUES.md:24` | — | — |
| `openissues--p2-toward-a-useful-development-agent-mvp` | section | — | P2 — Toward a useful development agent / MVP | `docs/OPEN_ISSUES.md:37` | — | — |
| `openissues--p3-production-oriented-track-only` | section | — | P3 — Production-oriented (track only) | `docs/OPEN_ISSUES.md:51` | — | — |
| `openissues--suggested-github-issue-titles` | section | — | Suggested GitHub issue titles | `docs/OPEN_ISSUES.md:64` | — | 1. [P0] Fix cabal-devmelopner-tui entrypoint (missing main) |
| `openissues--out-of-scope-for-the-docs-pr-that-added-this-file` | section | — | Out of scope for the docs PR that added this file | `docs/OPEN_ISSUES.md:77` | — | - Implementing the fixes above |
| `openissues--mvp-1-minimal-tools-started-chore-mvp1-tools-start-appended-2026-07-09` | section | MVP-1 | MVP-1 minimal tools started (chore/mvp1-tools-start appended 2026-07-09) | `docs/OPEN_ISSUES.md:82` | — | - Per plan.md p2 (cabal-poc-mvp): B1 tool host v0 (read/list/run + TOOL via EventBus) + B2 loop (model propose/execute/re-prompt) + tero/W2 integrate. |
| `openissues--status-alignment-post-w2-c0-pr12-appended-2026-07-09-chore-honest-docs-post-w2` | section | — | Status alignment post W2/C0 + PR#12 (appended 2026-07-09, chore/honest-docs-post-w2) | `docs/OPEN_ISSUES.md:91` | — | - POC-1 (TUI entrypoint) + POC-3 (real Task): addressed by A1/A2 in PR#12 cab/a1-a3 (now cabal-devmelopner-tui has main(); TUI imports/uses core.types.Task). |
| `openissues--poc-6-documented-as-single-shot-chore-poc6-iteration-honesty-appended` | section | POC-6 | POC-6 documented as single-shot (chore/poc6-iteration-honesty appended) | `docs/OPEN_ISSUES.md:100` | — | - Per plan.md (cabal section priority 2, "cabal-poc-mvp POC-6"): decide/document as single-shot (honest, defer full feedback to MVP/tools). Matches agent.py re… |
| `openissues--mvp-1-complete-chore-cabal-poc-mvp-close-appended-2026-07-09` | section | MVP-1 | MVP-1 complete (chore/cabal-poc-mvp-close appended 2026-07-09) | `docs/OPEN_ISSUES.md:109` | — | - Per plan.md priority 2 (cabal-poc-mvp): B1 tool host + B2 loop implemented/verified. |
| `release100` | section | — | Release checklist — v1.0.0 | `docs/RELEASE_1_0_0.md:1` | — | — |
| `release100--pre-tag-must-be-true` | section | — | Pre-tag (must be true) | `docs/RELEASE_1_0_0.md:3` | — | — |
| `release100--product-p0-from-v100gapanalysis` | section | — | Product P0 (from V1_0_0_GAP_ANALYSIS) | `docs/RELEASE_1_0_0.md:5` | — | — |
| `release100--interim-release` | section | — | Interim release | `docs/RELEASE_1_0_0.md:23` | — | - v0.2.0 (2026-07-21): ship leaf core without waiting for E7/E3.2. |
| `release100--honesty-bar` | section | — | Honesty bar | `docs/RELEASE_1_0_0.md:28` | — | - [ ] README / PHASE / OPENISSUES do not claim multi-agent swarm production or legitimate RAG via context-mcp |
| `release100--gates` | section | — | Gates | `docs/RELEASE_1_0_0.md:33` | — | ./scripts/check.sh --quick |
| `release100--optional-smoke-with-local-ollama-if-available` | other | — | optional: smoke with local ollama if available | `docs/RELEASE_1_0_0.md:38` | — | 1. Bump VERSION → 1.0.0 |
| `release100--versioning` | section | — | Versioning | `docs/RELEASE_1_0_0.md:41` | — | 1. Bump VERSION → 1.0.0 |
| `release100--compose-matrix-1.0` | section | — | Compose matrix (1.0) | `docs/RELEASE_1_0_0.md:50` | — | - [ ] Update fleet prefer-list warm to include this tag branch if needed |
| `release100--post-tag` | section | — | Post-tag | `docs/RELEASE_1_0_0.md:60` | — | - [ ] Update fleet prefer-list warm to include this tag branch if needed |
| `roadmap` | note | — | cabal-devmelopner — Product Roadmap | `docs/ROADMAP.md:1` | Plan (2026-07-08) | Status: Plan (2026-07-08) |
| `roadmap--1.-north-star` | section | — | 1. North star | `docs/ROADMAP.md:11` | — | cabal-devmelopner is a repo-agnostic development agent: long-running, event-driven, multi-surface (CLI / TUI / future Discord), with strong Tero integration fo… |
| `roadmap--2.-current-position-summary` | section | — | 2. Current position (summary) | `docs/ROADMAP.md:32` | — | PoC exit requires honest tests/stabilization (POC-7); iteration (POC-6) now documented single-shot (honest, per plan.md p2 deferral to MVP/tools); TUI launch (… |
| `roadmap--3.-architecture-target-incremental` | section | — | 3. Architecture target (incremental) | `docs/ROADMAP.md:49` | — | ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ |
| `roadmap--4.-waves` | section | — | 4. Waves | `docs/ROADMAP.md:84` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-a-poc-close-out-make-claims-true` | section | — | Wave A — PoC close-out (make claims true) | `docs/ROADMAP.md:86` | — | Goal: Documented entrypoints work; status docs match code; minimal regression net. |
| `roadmap--wave-b-minimum-useful-agent-mvp-core` | section | — | Wave B — Minimum useful agent (MVP core) | `docs/ROADMAP.md:107` | — | Goal: Agent can act on a repo with Tero-assisted context and a real loop. |
| `roadmap--mvp-1-tools-start-chore-mvp1-tools-start-2026-07-09-appended` | section | MVP-1 | MVP-1 tools start (chore/mvp1-tools-start, 2026-07-09 appended) | `docs/ROADMAP.md:129` | — | - B1: core/tools.py (ToolHost + readfile/listdir/runcommand allowlisted + parse + events TOOLCALL/RESULT). |
| `roadmap--mvp-1-complete-chore-cabal-poc-mvp-close-appended` | section | MVP-1 | MVP-1 complete (chore/cabal-poc-mvp-close appended) | `docs/ROADMAP.md:141` | — | - B1/B2 done + verified green: tools.py full host+parse+safe+events; agent loop tool detect/execute/re-prompt budget + feedback; cli --use-tools + events; prom… |
| `roadmap--wave-c-daily-co-dev-polish-mvp-complete` | section | — | Wave C — Daily co-dev polish (MVP complete) | `docs/ROADMAP.md:153` | — | Goal: Comfortable daily driver. |
| `roadmap--wave-d-multi-agent-production-shape` | section | — | Wave D — Multi-agent & production shape | `docs/ROADMAP.md:170` | — | Goal: Coordinated agents with safe concurrency; security load-bearing. |
| `roadmap--wave-updates-w2-facade-cabal-integration-2026-07-09` | section | — | Wave Updates (W2 Facade + Cabal Integration, 2026-07-09) | `docs/ROADMAP.md:187` | — | As part of wsfull PR process and doc/tero updates: |
| `roadmap--5.-dependency-graph-high-level` | section | — | 5. Dependency graph (high level) | `docs/ROADMAP.md:205` | — | Wave A (PoC honest) |
| `roadmap--6.-pr-plan-incremental-reviewable` | section | — | 6. PR Plan (incremental, reviewable) | `docs/ROADMAP.md:224` | — | Each PR should be independently mergeable to dev. Suggested titles match GitHub issues where they exist. |
| `roadmap--wave-a` | section | — | Wave A | `docs/ROADMAP.md:228` | — | — |
| `roadmap--wave-b` | section | — | Wave B | `docs/ROADMAP.md:240` | — | — |
| `roadmap--wave-c` | section | — | Wave C | `docs/ROADMAP.md:253` | — | — |
| `roadmap--wave-d` | section | — | Wave D | `docs/ROADMAP.md:262` | — | — |
| `roadmap--7.-key-decisions` | section | — | 7. Key decisions | `docs/ROADMAP.md:274` | — | — |
| `roadmap--8.-open-questions-need-maintainer-input` | section | — | 8. Open questions (need maintainer input) | `docs/ROADMAP.md:289` | — | 1. Default tool allowlist — shell unrestricted vs allowlist-only from day one? (Recommend allowlist-only.) |
| `roadmap--9.-suggested-near-term-execution-order-next-2-weeks` | section | — | 9. Suggested near-term execution order (next 2 weeks) | `docs/ROADMAP.md:299` | — | 1. Land docs PR #1 (intent/gap + cold-start) if not merged. |
| `roadmap--10.-success-metrics-lightweight` | section | — | 10. Success metrics (lightweight) | `docs/ROADMAP.md:310` | — | — |
| `roadmap--11.-references-tero-cited` | section | — | 11. References (Tero-cited) | `docs/ROADMAP.md:320` | — | Local product docs: PHASE, INTENTANDGAPANALYSIS, OPENISSUES, TERO. |
| `roadmap--appended-pr12-w2-facade-c0-resolution-2026-07-09` | section | — | Appended: PR#12 W2 facade + C0 resolution (2026-07-09) | `docs/ROADMAP.md:334` | — | - Integrated W2 schemas (Structured, Citation, MemoryContext) + CommonMemoryAdapter + AgentDomain M1 (6+ domains incl. TERO/CONTEXT/MEMORYGATE/LANG). |
| `roadmap--honest-docs-update-chore-honest-docs-post-w2` | section | — | Honest docs update (chore/honest-docs-post-w2) | `docs/ROADMAP.md:341` | — | - Aligned lagging current-position table + Wave A exit text post-PR#12 merges (TUI entrypoint now accurate; POC-1/3/4 closed in code). |
| `roadmap--poc-6-documented-single-shot-chore-poc6-iteration-honesty-per-plan.md-p2` | section | POC-6 | POC-6 documented single-shot (chore/poc6-iteration-honesty per plan.md p2) | `docs/ROADMAP.md:348` | — | - A6 marked documented single-shot; footnote updated; exit/position text revised for honesty (no longer requires POC-6 for PoC exit). |
| `roadmap--dev-mcp-orch-wiring-cabal-as-leaf-consumer-chore-orch-wiring-devmcp` | section | — | dev-mcp Orch Wiring (cabal as leaf consumer; chore/orch-wiring-devmcp) | `docs/ROADMAP.md:356` | — | Appended notes on dev-mcp orch use per task (parallel to W2 docs): |
| `securityreview10` | section | — | Security review checklist — cabal-devmelopner 1.0 | `docs/SECURITY_REVIEW_1_0.md:1` | Living checklist for E8.2. Complete before `v1.0.0` tag. | Status: Living checklist for E8.2. Complete before v1.0.0 tag. |
| `securityreview10--scope` | section | — | Scope | `docs/SECURITY_REVIEW_1_0.md:6` | — | Leaf coding agent: CLI/TUI, optional Tero client, ToolHost (fs + allowlisted commands), |
| `securityreview10--checklist` | section | — | Checklist | `docs/SECURITY_REVIEW_1_0.md:12` | — | — |
| `securityreview10--secrets-credentials` | section | — | Secrets & credentials | `docs/SECURITY_REVIEW_1_0.md:14` | — | — |
| `securityreview10--filesystem-confinement-toolhost` | section | — | Filesystem confinement (ToolHost) | `docs/SECURITY_REVIEW_1_0.md:23` | — | — |
| `securityreview10--command-execution` | section | — | Command execution | `docs/SECURITY_REVIEW_1_0.md:32` | — | — |
| `securityreview10--network-providers` | section | — | Network & providers | `docs/SECURITY_REVIEW_1_0.md:40` | — | — |
| `securityreview10--supply-chain-ci` | section | — | Supply chain / CI | `docs/SECURITY_REVIEW_1_0.md:47` | — | ./scripts/check.sh --quick |
| `securityreview10--spot-check-procedure` | section | — | Spot-check procedure | `docs/SECURITY_REVIEW_1_0.md:55` | — | ./scripts/check.sh --quick |
| `securityreview10--sign-off` | section | — | Sign-off | `docs/SECURITY_REVIEW_1_0.md:63` | — | When all boxes are ☑ and tests green, E8.2 is complete for 1.0 ship. |
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
| `toolingstackreadiness` | section | — | Tooling stack readiness — cabal 1.0 workflow efficiency | `docs/TOOLING_STACK_READINESS.md:1` | — | Date: 2026-07-21 |
| `toolingstackreadiness--1.-stack-map-roles` | section | — | 1. Stack map (roles) | `docs/TOOLING_STACK_READINESS.md:10` | — | flowchart TB |
| `toolingstackreadiness--memory-pipeline-target-not-all-wired-yet` | section | — | Memory pipeline (target — not all wired yet) | `docs/TOOLING_STACK_READINESS.md:42` | — | flowchart LR |
| `toolingstackreadiness--2.-efficiency-gaps-tooling-not-cabal-core` | section | — | 2. Efficiency gaps (tooling, not cabal core) | `docs/TOOLING_STACK_READINESS.md:89` | — | — |
| `toolingstackreadiness--3.-minimum-tooling-up-to-snuff-checklist-before-heavy-1.0-impl` | section | — | 3. Minimum “tooling up to snuff” checklist (before heavy 1.0 impl) | `docs/TOOLING_STACK_READINESS.md:104` | — | - [x] gha-runner-ctl 0.2.10 pool live (16c/16g) |
| `toolingstackreadiness--must-blocks-efficient-joint-work` | section | — | Must (blocks efficient joint work) | `docs/TOOLING_STACK_READINESS.md:106` | — | - [x] gha-runner-ctl 0.2.10 pool live (16c/16g) |
| `toolingstackreadiness--should-within-first-1.0-weeks-after-tools` | section | — | Should (within first 1.0 weeks, after tools) | `docs/TOOLING_STACK_READINESS.md:117` | — | - [ ] tero-rs --features memory + memory-gate-rs integration smoke |
| `toolingstackreadiness--later` | section | — | Later | `docs/TOOLING_STACK_READINESS.md:126` | — | - [ ] security-mcp wrap of runcommand |
| `toolingstackreadiness--4.-recommended-joint-ops-claude-grok` | section | — | 4. Recommended joint ops (Claude + Grok) | `docs/TOOLING_STACK_READINESS.md:133` | — | — |
| `toolingstackreadiness--5.-immediate-actions-this-tranche` | section | — | 5. Immediate actions (this tranche) | `docs/TOOLING_STACK_READINESS.md:144` | — | 1. Land cabal docs PR: V1 gap + joint exec + this readiness file. |
| `toolingstackreadiness--6.-bottom-line` | section | — | 6. Bottom line | `docs/TOOLING_STACK_READINESS.md:153` | — | The runtime fleet (gha-runner-ctl, tg-agent-relay) is good enough to execute cabal 1.0 efficiently. The product leaf (cabal) is the bottleneck (write/verify/st… |
| `v100gapanalysis` | section | — | cabal-devmelopner — 1.0.0 Gap Analysis | `docs/V1_0_0_GAP_ANALYSIS.md:1` | — | Baseline: dev @ 5fd9781 (fleet harden) + product tree ~2.0 kLOC under src/cabaldevmelopner/ |
| `v100gapanalysis--1.-what-1.0.0-means-product-definition` | section | — | 1. What 1.0.0 means (product definition) | `docs/V1_0_0_GAP_ANALYSIS.md:14` | — | 1.0.0 = daily co-dev agent you can trust on a real repo without hand-copying model output. |
| `v100gapanalysis--execution-order-maintainer-direction-2026-07-21` | section | — | Execution order (maintainer direction 2026-07-21) | `docs/V1_0_0_GAP_ANALYSIS.md:46` | — | 1. Tools usable — write/applypatch + multi-step loop + verify (E1 → E2) |
| `v100gapanalysis--2.-current-reality-0.1.0-measured-2026-07-21` | section | — | 2. Current reality (0.1.0 — measured 2026-07-21) | `docs/V1_0_0_GAP_ANALYSIS.md:53` | — | — |
| `v100gapanalysis--3.-gap-matrix-1.0.0` | section | — | 3. Gap matrix → 1.0.0 | `docs/V1_0_0_GAP_ANALYSIS.md:87` | — | — |
| `v100gapanalysis--github-issues-hygiene-filed-vs-reality` | section | — | GitHub issues hygiene (filed vs reality) | `docs/V1_0_0_GAP_ANALYSIS.md:106` | — | — |
| `v100gapanalysis--4.-epics-for-1.0.0-github-milestone-v1.0.0` | section | — | 4. Epics for 1.0.0 (GitHub milestone `v1.0.0`) | `docs/V1_0_0_GAP_ANALYSIS.md:120` | — | Outcome: Versioning, CI gates, docs SoT, milestone hygiene. |
| `v100gapanalysis--epic-e0-release-foundation-ship` | section | — | Epic E0 — Release foundation (Ship) | `docs/V1_0_0_GAP_ANALYSIS.md:122` | — | Outcome: Versioning, CI gates, docs SoT, milestone hygiene. |
| `v100gapanalysis--epic-e1-act-on-codebases-tools-v1` | section | — | Epic E1 — Act on codebases (Tools v1) | `docs/V1_0_0_GAP_ANALYSIS.md:132` | — | Outcome: Agent can modify a repo safely. |
| `v100gapanalysis--epic-e2-verify-loop` | section | — | Epic E2 — Verify loop | `docs/V1_0_0_GAP_ANALYSIS.md:143` | — | Outcome: Edits are checked, not trusted. |
| `v100gapanalysis--epic-e3-config-budgets-packaging` | section | — | Epic E3 — Config, budgets, packaging | `docs/V1_0_0_GAP_ANALYSIS.md:152` | — | Outcome: Installable, tunable leaf. |
| `v100gapanalysis--epic-e4-providers-streaming` | section | — | Epic E4 — Providers & streaming | `docs/V1_0_0_GAP_ANALYSIS.md:162` | — | Outcome: Local default, frontier optional, progressive UX. |
| `v100gapanalysis--epic-e5-tero-memory-honesty` | section | — | Epic E5 — Tero & memory honesty | `docs/V1_0_0_GAP_ANALYSIS.md:171` | — | Outcome: Opt-in context that never lies. |
| `v100gapanalysis--epic-e6-tui-v1` | section | — | Epic E6 — TUI v1 | `docs/V1_0_0_GAP_ANALYSIS.md:181` | — | Outcome: Daily co-dev surface. |
| `v100gapanalysis--epic-e7-notify-hitl` | section | — | Epic E7 — Notify + HITL | `docs/V1_0_0_GAP_ANALYSIS.md:191` | — | Outcome: Async awareness + approval. |
| `v100gapanalysis--epic-e8-hardening-for-1.0-ship` | section | — | Epic E8 — Hardening for 1.0 ship | `docs/V1_0_0_GAP_ANALYSIS.md:200` | — | Outcome: Trust. |
| `v100gapanalysis--5.-suggested-issue-graph-disjoint-by-design` | section | — | 5. Suggested issue graph (disjoint by design) | `docs/V1_0_0_GAP_ANALYSIS.md:212` | — | flowchart TB |
| `v100gapanalysis--6.-definition-of-done-for-1.0.0` | section | — | 6. Definition of Done for 1.0.0 | `docs/V1_0_0_GAP_ANALYSIS.md:241` | — | - [ ] All P0 issues under E0–E8 closed |
| `v100gapanalysis--7.-effort-sketch-indicative` | section | — | 7. Effort sketch (indicative) | `docs/V1_0_0_GAP_ANALYSIS.md:253` | — | — |
| `v100gapanalysis--8.-open-decisions-need-deliberation` | section | — | 8. Open decisions (need deliberation) | `docs/V1_0_0_GAP_ANALYSIS.md:271` | — | 1. Write tool shape: full file write vs unified diff apply only? (Recommend diff/apply first for safer review.) |
| `v100gapanalysis--9.-bottom-line` | section | — | 9. Bottom line | `docs/V1_0_0_GAP_ANALYSIS.md:281` | — | Today (0.1.0): honest config + tools-read scaffold + dual provider + Tero opt-in — a strong architecture alpha, not yet a 1.0 development agent. |
| `v100jointexecution` | section | — | Joint execution plan — Grok + Claude Code (1.0.0) | `docs/V1_0_0_JOINT_EXECUTION.md:1` | — | Purpose: Disjoint-by-design implementation after [V100GAPANALYSIS.md](V100GAPANALYSIS.md). |
| `v100jointexecution--rules-both-agents` | section | — | Rules (both agents) | `docs/V1_0_0_JOINT_EXECUTION.md:8` | — | 1. One worktree per leaf; never commit on main/dev directly. |
| `v100jointexecution--lane-ownership` | section | — | Lane ownership | `docs/V1_0_0_JOINT_EXECUTION.md:19` | — | Conflict resolution: L0 (cabal/Grok orchestrator) reassigns paths; never force-push shared branches. |
| `v100jointexecution--phase-0-bookkeeping-l-ops-started` | section | — | Phase 0 — Bookkeeping — **L-ops** ✅ started | `docs/V1_0_0_JOINT_EXECUTION.md:32` | — | - [x] Milestone v1.0.0 + epics #19–#27 |
| `v100jointexecution--phase-1-tools-usable-first-l-core` | section | — | Phase 1 — Tools usable **FIRST** — **L-core** | `docs/V1_0_0_JOINT_EXECUTION.md:39` | — | — |
| `v100jointexecution--phase-1b-memory-stack-usable-parallel-after-tools-land` | section | — | Phase 1b — Memory stack usable (parallel after tools land) | `docs/V1_0_0_JOINT_EXECUTION.md:50` | — | — |
| `v100jointexecution--phase-2-stream-session-tui` | section | — | Phase 2 — Stream + Session + TUI | `docs/V1_0_0_JOINT_EXECUTION.md:60` | — | — |
| `v100jointexecution--landed-on-dev-2026-07-21` | section | — | Landed on `dev` (2026-07-21) | `docs/V1_0_0_JOINT_EXECUTION.md:69` | — | — |
| `v100jointexecution--phase-3-polish-ship` | section | — | Phase 3 — Polish + Ship | `docs/V1_0_0_JOINT_EXECUTION.md:82` | — | — |
| `v100jointexecution--claude-code-kickoff-blurb-paste` | section | — | Claude Code kickoff blurb (paste) | `docs/V1_0_0_JOINT_EXECUTION.md:93` | — | You are L1 implementer for cabal-devmelopner 1.0.0. |
| `v100jointexecution--grok-kickoff-blurb-self` | section | — | Grok kickoff blurb (self) | `docs/V1_0_0_JOINT_EXECUTION.md:104` | — | You are L0/L-ops + L-memory for cabal-devmelopner 1.0.0. |
| `v100jointexecution--exit-of-this-plan-doc` | section | — | Exit of this plan doc | `docs/V1_0_0_JOINT_EXECUTION.md:114` | — | When Phase 0 issues exist on GitHub and Phase 1 first PR is open, this plan is active. Update checkboxes as waves complete (append-only notes at bottom). |
| `readme-2` | other | — | Tero index (Layer 1) | `docs/tero-index/README.md:1` | — | Machine + human citation index for this repository. |
| `readme--regenerate` | section | — | Regenerate | `docs/tero-index/README.md:13` | — | python3 /path/to/tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--or-if-tero-mcp-is-a-sibling` | other | — | or if tero-mcp is a sibling: | `docs/tero-index/README.md:17` | — | python3 ../tero-mcp/scripts/generateliteindex.py --root $(pwd) |
| `readme--serve-locally` | section | — | Serve locally | `docs/tero-index/README.md:21` | — | export TEROTOKENS=local-dev:refresh |

## changelog (12 entries)

| Anchor | Kind | Id | Title | File:Line | Status | Summary |
|---|---|---|---|---|---|---|
| `changelog` | entry | — | Changelog | `CHANGELOG.md:1` | — | All notable changes to cabal-devmelopner are documented in this file. |
| `changelog--unreleased` | section | — | [Unreleased] | `CHANGELOG.md:8` | — | - E7.3 HITL approve path; E6.2 cancel |
| `changelog--planned-toward-1.0.0` | section | — | Planned toward 1.0.0 | `CHANGELOG.md:10` | — | - E7.3 HITL approve path; E6.2 cancel |
| `changelog--0.2.1-2026-07-21` | section | — | [0.2.1] — 2026-07-21 | `CHANGELOG.md:16` | — | Patch release: outbound Telegram notify + soft wall-clock budget (merged from #36). |
| `changelog--added` | section | — | Added | `CHANGELOG.md:20` | — | - E7.1 notify: cabaldevmelopner.notify.RelayNotifier calls tg-agent-relay |
| `changelog--changed` | section | — | Changed | `CHANGELOG.md:30` | — | - cabal.example.toml documents [notify] and wall budget knobs. |
| `changelog--0.2.0-2026-07-21` | section | — | [0.2.0] — 2026-07-21 | `CHANGELOG.md:34` | — | Interim leaf agent release: act + verify + session + stream + TUI dogfood. |
| `changelog--added-2` | section | — | Added | `CHANGELOG.md:39` | — | - Tools write path: writefile / applypatch workspace-confined (E1.1) |
| `changelog--changed-2` | section | — | Changed | `CHANGELOG.md:56` | — | - README honesty for 0.2.0 feature set |
| `changelog--product-status-honest` | section | — | Product status (honest) | `CHANGELOG.md:61` | — | — |
| `changelog--0.1.0-2026-07-16` | section | — | [0.1.0] — 2026-07-16 | `CHANGELOG.md:76` | — | - Config-as-code: cabal.example.toml with L0 / L1 profiles |
| `changelog--added-3` | section | — | Added | `CHANGELOG.md:78` | — | - Config-as-code: cabal.example.toml with L0 / L1 profiles |

