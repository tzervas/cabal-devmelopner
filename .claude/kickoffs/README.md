# cabal-devmelopner local kickoffs (leaf under wsfull orchestrator)

This is a **leaf kickoff** managed by the central workspace orchestrator (`wsfull`).

See root `/root/git/.claude/kickoffs/wsfull.md` (orchestrator flow) + `cab.md` for the stowed brief.

**How it runs**:
- wsfull spawns an isolated worktree for this leaf (worktree-guard).
- Work on your working branch inside the worktree.
- Change-scoped work + tests + **early security scans** (patch vulns immediately).
- PR the polished result to this repo's `dev`.
- Orchestrator (wsfull) will pull it into dev for wiring/integration + full integration/regression testing (incl. security).

Local notes:
- Run from inside: uv sync; use local tero-index.
- Tero-first: always (categories help).
- Guard + dev-workflow for changes.
- PR to dev (change-scoped tested).

Additional local stows can live here (e.g. cab-tui.md) for finer waves.

## Latest Updates (as of 2026-07-09, part of PR process)

- W2 CommonMemory facade implementation: CommonMemoryAdapter + AgentDomain M1 (Py mirror from memory-gate-rs M1 domains: TERO, CONTEXT, MEMORY_GATE, LANG_*, WORKSPACE etc.) in core/schemas.py (generated via codegen from dev-docs/schemas/).
- Wired in agent: SimpleAgent.run_structured uses facade.query(AgentDomain.TERO, ...) for mem_contexts + StructuredResponse (W2 schemas: Citation, MemoryContext, StructuredPrompt/Response) with citations; legacy compat kept. Errors surfaced (A2/POC-8 + C0 honesty).
- PR #12: cab/a1-a3-tui-errors-tests → dev (includes facade, agent/prompt/tero_client wiring, A1-A3 TUI/errors/tests, doc updates, tero reindex).
- Integration via cabal + tero: auto tero index discovery; full workspace targets ready (from WORKSPACE_CABAL_TERO_READINESS.md); dual tero + domains.
- Hygiene, security-scan, C0/M1: applied (ctx C0 honesty gate, mint M1 facade, parameterized skills); checks/ruff green.
- Kickoffs, agent context (AGENTS.md), claude files updated to latest (facade, W2 schemas, tero-first, dev-workflow, branch/worktree guards).
- Docs updated: AGENTS.md, README.md, docs/ROADMAP.md, docs/INTENT_AND_GAP_ANALYSIS.md, docs/TERO.md, PHASE.md, this .claude/kickoffs/README.md. References to facade, W2, tero-first, dev-workflow, guards.
- Tero indexes updated post-docs (run /root/git/scripts/update-tero.sh); included in PR.
- State from wsfull-wave-2026-07-09-compact.md + WORKSPACE_CABAL_TERO_READINESS.md: branches pushed, local models (ollama default + tero + W2), parameterized skills (hygiene etc), readiness.
- Review via pr-review skill (adapted from mycelium to workspace: tero citations, W2/StructuredResponse, CommonMemory facade, C0 gate, M1 domains, dev-workflow, guards, hygiene/security, append-only, tero-first); if +ve, gh pr merge --auto.
- Use: tero + W2 + local-ollama preferred. Follow dev-workflow, branch-guard, worktree-guard, hygiene, security-scan, tero-first always.

Run updates, tero regen, commit+push to branch to update PR before review/merge.

Tero-first: ./scripts/tero.sh cabal-devmelopner text_search "facade" etc. See dev-docs for sources.

## Post-fix append (2026-07-09)

- Fixed C0 blocker in PR#12 (facade error now properly emits ERROR via agent when refusal returned from query; test updated + green).
- Per user: docs/kickoffs/AGENTS/claude + all docs updated as part of PR process for each repo.
- Run update-tero included.
- One agent per PR for review+merge via adapted pr-review skill + rubric (tero/W2/C0/M1/dev-workflow/guards).
- Then merge up + propagate pulls to core (dev/main) lowers.
- Swarm used for broad disjoint repo tasks.
- See wsfull.md + private-docs/analyses/ for status. All append-only, tero-cited, guards.

## Review+Merge Complete (2026-07-09, dedicated agent)

- Tero-first executed (MCP tero__* + /root/git/scripts/tero.sh for "cabal W2 facade" "C0" "PR#12"; cited dev-docs/wsfull-wave-2026-07-09-compact.md + WORKSPACE_CABAL_TERO_READINESS.md).
- pr-review rubric applied: T2; full report posted as gh comment on #12; PR body edited.
- No Critical blockers (C0 resolved: agent.py + schemas.py + test green; W2 StructuredResponse contract holds).
- Merge: gh pr merge 12 (MERGED).
- Post-steps executed on dev: update-tero.sh (150 items), hygiene (ruff + pytest 6/6 green).
- This file + AGENTS.md + cab.md (root) appended (append-only).
- re-ran update-tero.sh cabal-devmelopner.
- Status: PR#12 + review+merge landed. Cites: agents--pr12-review-merge-2026-07-09 (AGENTS.md), workspacecabalteroreadiness sections.

