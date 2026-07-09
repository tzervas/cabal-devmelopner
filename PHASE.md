# cabal-devmelopner — Development Phases

This document tracks the phased development of `cabal-devmelopner`.

For honest status vs intent (including known P0/P1 gaps), see **[docs/INTENT_AND_GAP_ANALYSIS.md](docs/INTENT_AND_GAP_ANALYSIS.md)** and the backlog in **[docs/OPEN_ISSUES.md](docs/OPEN_ISSUES.md)**.

**Full product plan (waves + PR DAG):** **[docs/ROADMAP.md](docs/ROADMAP.md)** — maps PoC → MVP → Production onto ordered work, with Tero/corpus alignment.

---

## PoC Phase (Current)

**Goal**: Validate core architecture and get a working, extensible agent.

### Deliverables

- [x] Project skeleton + installable CLI
- [x] Event/communication system (producer/consumer model)
- [x] xAI provider (raw API)
- [~] Improved agent loop with iteration + feedback — *documented as single-shot per POC-6 decision (plan.md p2); loop scaffold only, always returns after iter 1; full feedback deferred to MVP/tools (see POC-6)*

## Recent Wave Updates (W2 Facade + Integration, 2026-07-09)

As part of wsfull PR process:
- W2 CommonMemory facade implementation + AgentDomain M1 (mirror memory-gate-rs): CommonMemoryAdapter + Structured* W2 schemas (Citation/MemoryContext/StructuredResponse etc) in schemas.py.
- Wiring in agent: facade.query(AgentDomain.TERO..) drives memory + structured in run_structured (C0 honesty, error surfacing).
- PR #12 (cab/a1-a3-tui-errors-tests): facade + A1-A3 TUI/errors/tests + wiring + doc updates (AGENTS, README, docs/ROADMAP, INTENT_AND_GAP_ANALYSIS, TERO, PHASE, .claude/kickoffs/README.md) + tero reindex.
- Integration via cabal + tero (local index), hygiene, C0 (honesty gate), M1 domains.
- Kickoffs, agent context (AGENTS.md), claude files updated to latest (facade/W2 refs, tero-first, dev-workflow, branch/worktree guards).
- Docs + tero updated as part of PR process; run update-tero after edits.
- See wsfull-wave-2026-07-09-compact.md (W2, local-ollama+tero+W2 pipeline, parameterized hygiene/security-scan/codegen, leaf C0/M1), WORKSPACE_CABAL_TERO_READINESS.md (facade cabal integration, tero readiness).
- Review via adapted pr-review skill (tero citations, W2 schemas/StructuredResponse, CommonMemory facade, C0 gate, M1, dev-workflow, guards, hygiene/security, append-only, tero-first); merge if +ve.
- Tero-first, dev-workflow, guards followed for changes.

See compact, readiness, PR for details. Update docs + tero before land.
- [x] Basic prompt construction
- [~] Tero-MCP client integration — *opt-in client + docs + W2 facade (CommonMemoryAdapter + AgentDomain); requires sibling `tero-mcp` + local index (see [docs/TERO.md](docs/TERO.md)); errors now surfaced via EventBus.ERROR (C0/POC-4 fixed in PR#12; facade returns explicit refusal per W2 contract)*
- [~] Minimal TUI foundation — *UI present + functional entrypoint (A1); uses real Task dataclass (POC-3/A2); error surfacing (A3) — fixed in PR#12 (cab/a1-a3-tui-errors-tests); still PoC surface (full features in Wave B)*
- [x] Basic documentation and usage examples ([README](README.md), [docs/TERO.md](docs/TERO.md), [AGENTS.md](AGENTS.md), intent/gap docs)
- [ ] PoC testing and stabilization (POC-7)

`[x]` done · `[~]` partial / conditional · `[ ]` not done

### Exit Criteria

| Criterion | Status |
|-----------|--------|
| Can run `cabal-devmelopner "some task"` and get useful output from Grok | **Partial** — single-shot completion; no repo edits |
| Architecture is clean and extensible | **Directional** — seams in place |
| Tero-MCP can be called from the agent | **Conditional** — `--use-tero` / `USE_TERO=true` with sibling layout |
| TUI launches via documented entrypoints | **Met (PoC)** — `cabal-devmelopner-tui` entrypoint + Task wiring fixed in PR#12 (A1-A3/POC-1/POC-3); full TUI polish later |

**PoC not exited** until testing/stabilization (POC-7) are honest; iteration/feedback (POC-6) is now documented as single-shot (honest deferral to MVP/tools per plan.md); TUI entrypoint (POC-1) + Tero error surfacing (POC-4) addressed in PR#12. See wsfull-wave-2026-07-09-compact.md , WORKSPACE_CABAL_TERO_READINESS.md and plan.md (cabal-poc-mvp).

---

## MVP Phase

**Goal**: Make `cabal-devmelopner` a practical daily co-dev tool.

### Key Features

- Full-featured TUI (status, progress, logs, task management)
- Solid context management using Tero-MCP
- Easy configuration system
- Notification channels (Discord webhook + Telegram)
- Improved agent loop with real verification/feedback
- Basic support for running as a long-lived process
- Packaging and easy installation (`uv tool install`)
- Minimal tool use so the agent can act on a codebase (see MVP-1; started in chore/mvp1-tools-start: read_file/list_dir/run_command allowlisted + loop + TOOL_* events + --use-tools)

### Exit Criteria

- Comfortable to use for real development work.
- Can run for extended periods with decent context handling.
- Notifications work reliably.

---

## Production Phase

**Goal**: Robust, scalable, multi-agent development system.

### Key Features

- Multi-provider support (xAI, Claude, others)
- Full Discord control (task submission, monitoring, approvals)
- Agent swarm orchestration (multiple swarms running simultaneously)
- Wave-based execution patterns ("wave n" style)
- Safe concurrent file modification ("lowest common owner" model)
- Advanced Tero + Context MCP integration (including embeddings + true RAG)
- Resource management (memory, disk, context windows)
- Security layer (hardwired wrapping of tools like webpuppet via Security MCP)
- Persistent state and session management
- High reliability and polish

### Exit Criteria

- Can reliably run long development sessions with minimal human intervention.
- Supports complex workflows involving multiple coordinated agents.
- Security and resource protections are load-bearing.

---

## Notes

- All phases should maintain the core principles: repo-agnostic, extensible communications, strong Tero integration, and clean architecture.
- Security and resource management concerns should be considered from MVP onward, even if full implementation lands in Production.
- Prefer updating checkboxes here when code lands; keep narrative detail in the intent/gap analysis.

## MVP-1 tools start (appended 2026-07-09, chore/mvp1-tools-start per plan.md p2)
- Started B1 (tool host v0 in core/tools.py: read/list/run allowlisted, emit TOOL_*) + B2 (agent loop detect/execute/feedback re-prompt).
- Wired --use-tools (cli), tool instr in prompts (with tero/W2), basic tests, events visible.
- Agent still single-shot when !tools (honest); full iter feedback + verify deferred (B4).
- Followed: Tero-first (script + mcp identify/search), append-only, branch from main, dev-workflow/guards.
- Update-tero + hygiene after; land --no-ff dev/main + propagate.
- Cites: plan.md (B1/B2 + integrate tero/W2), ROADMAP Wave B, OPEN_ISSUES MVP-1, AGENTS.md, wsfull-wave-2026-07-09-compact.md.
- Status: MVP-1 minimal tools in progress (functional core); see ROADMAP for B3+.
- Tero cite post: phase--mvp-1-tools-start... + openissues etc.

### Appended: W2 + C0 fix for PR#12 (2026-07-09)
- W2 facade + AgentDomain + StructuredResponse wired + C0 error emit fixed (agent.py + test green).
- Part of cab branch PR#12 to dev. Docs/AGENTS/kickoffs updated per process.
- After tero update + checks: pr-review (rubric adapted for workspace tero/W2/C0/M1/guards) + merge.
- Tero-cited from wsfull compact + readiness (see dev-docs). dev-workflow + guards followed.

### Honest PoC status alignment (chore/honest-docs-post-w2, 2026-07-09)
- Updated lagging PoC bullets + exit criteria for TUI (now entrypoint + Task met post A1-A3) and Tero error handling (C0/POC-4 addressed, facade path).
- Iteration (POC-6) remains scaffold-only (always early return on iter 1); tests expanded (POC-7/A5 partial progress, 6+ smoke incl error paths) but stabilization open.
- Cross-cites: wsfull-wave-2026-07-09-compact.md (W2, C0/M1, PR#12, A1-A3), WORKSPACE_CABAL_TERO_READINESS.md (facade integration post-wave), AGENTS.md (post C0 + PR#12 review-merge).
- Append-only + tero-first (MCP text_search "W2 Facade"/"C0"/"wsfull-wave"); no code changes. See ROADMAP/INTENT/OPEN_ISSUES for parallel updates. Process: main pull, branch, edits, check.sh --quick, signed commit, PR to main.
- Tero cite ref: agents--pr12-review-merge-2026-07-09 + workspacecabalteroreadiness sections. Guards/dev-workflow followed.

### POC-6 iteration honesty (chore/poc6-iteration-honesty, per plan.md p2)
- **Decision:** Document POC-6 as single-shot (honest); defer full multi-iteration feedback + verification loop to MVP/tools (Wave B: B2/B4 etc). Matches code reality in agent.py (early return on iter==1; "PoC: first success").
- Updated deliverables status + exit criteria note. No code change (single-shot is intentional until tools).
- Cross-cites: /root/git/workspace/plan.md (cabal section: "POC-6 (P1): ... document single-shot (honest) ... update PHASE/ROADMAP..."), wsfull-wave-2026-07-09-compact.md, WORKSPACE_CABAL_TERO_READINESS.md, ROADMAP.md §Wave A A6.
- Tero-first: script + MCP identify/text_search ("POC","plan") before edits (refusals on "POC-6" pre-update as expected).
- Process: branch from main, append-only + targeted marks, checks, update-tero, land dev/main --no-ff.
- Tero cite target post-update: will hit after /root/git/scripts/update-tero.sh cabal-devmelopner (cites phase--*, openissues--*, roadmap--*, etc).
- Follows AGENTS.md (tero-first, dev-workflow, append-only, branch-guard, update this+tero), prior honest-docs-post-w2 pattern.
