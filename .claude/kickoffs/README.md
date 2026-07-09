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
