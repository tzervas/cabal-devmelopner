# Joint execution plan — Grok + Claude Code (1.0.0)

**Purpose:** Disjoint-by-design implementation after [V1_0_0_GAP_ANALYSIS.md](V1_0_0_GAP_ANALYSIS.md).  
**Orchestration:** Cabal Telegram (`@cabal`) for L0 status; Claude Code CLI as L1 implementer; Grok for ops/docs/memory/CI and parallel leaves.

---

## Rules (both agents)

1. **One worktree per leaf**; never commit on `main`/`dev` directly.  
2. **File ownership** per slice — no overlapping paths between concurrent agents.  
3. **Tero-first** when excavating siblings (tero-mcp, agent-harness, tg-agent-relay).  
4. **Self-hosted CI only:** `runs-on: [self-hosted, linux, x64, podman]` (+ size labels only if justified).  
5. **Honesty:** no claiming RAG/swarm/write until code lands.  
6. **PR size:** one epic-child issue per PR when possible; land leaf → `dev` with `--no-ff` or squash per repo norm.

---

## Lane ownership

| Lane | Primary | Secondary | Paths (exclusive while active) |
|------|---------|-----------|--------------------------------|
| **L-core** | Claude Code | Grok review | `src/cabal_devmelopner/core/{tools,agent,config,prompt}.py`, `tests/test_tools*.py` |
| **L-surface** | Claude Code | Grok | `providers/`, `tui/`, `cli.py` (stream flags only when L-core not touching cli) |
| **L-memory** | Grok | Claude review | `mcp/`, `core/session.py` (new), `docs/TERO.md`, session tests |
| **L-ops** | Grok | — | `.github/`, `docs/V1_*`, `docs/RELEASE*`, `scripts/`, notify module, packaging |

**Conflict resolution:** L0 (cabal/Grok orchestrator) reassigns paths; never force-push shared branches.

---

## Phase 0 — Bookkeeping — **L-ops** ✅ started

- [x] Milestone **v1.0.0** + epics #19–#27  
- [x] Close stale #2–#5,#7–#8  
- [x] Merge docs PR #28 when green  
- [x] compose-doctor + prefer/warm  

## Phase 1 — Tools usable **FIRST** — **L-core**

| Order | Issue | Owner |
|------:|-------|--------|
| 1 | E1.1 write_file + apply_patch | Grok (in #28 tools write) ✅ |
| 2 | E1.3 multi-step tools loop | pre-existing MVP-1 loop ✅ |
| 3 | E1.2 structured tool protocol | still free-text `call tool …` (Claude optional) |
| 4 | E2.1–E2.2 verify_command loop | Grok **PR #29 merged** ✅ |
| 5 | E3.1 budgets from cabal.toml | Grok **PR #29 merged** ✅ |
| — | CI babysit | Grok |

## Phase 1b — Memory stack usable (parallel after tools land)

| Order | Work | Repo | Status |
|------:|------|------|--------|
| 1 | Real Embedder + local backend (C1.x) | **context-mcp** | **PR #46 open** (Wave 1 trait + fail-closed) |
| 2 | tero-rs `memory` feature ↔ memory-gate-rs | tero-rs / memory-gate-rs | **smoked** store/retrieve 2026-07-21 |
| 3 | tero-mcp delegates memory_* to tero-rs | tero-mcp | lite refuses; binary path smoke ✅ |
| 4 | cabal facade: tero L1 + context-mcp + MG domains | cabal E5 | not started |
| 5 | Eval vs keyword baseline before RAG claims | context-mcp | Wave 2+ |

## Phase 2 — Stream + Session + TUI

| Issue | Owner |
|-------|--------|
| E4.1 streaming | Claude |
| E5.3 JSONL session | Grok |
| E5.1 tero zero-config errors | Grok |
| E6.1 TUI log/status | Claude |

## Phase 3 — Polish + Ship

| Issue | Owner |
|-------|--------|
| E6.2–E6.4 TUI cancel/thread | Claude |
| E7.1 Telegram notify | Grok |
| E7.3 HITL | Claude |
| E8.* release | Joint |

---

## Claude Code kickoff blurb (paste)

```text
You are L1 implementer for cabal-devmelopner 1.0.0.
SoT: docs/V1_0_0_GAP_ANALYSIS.md + docs/V1_0_0_JOINT_EXECUTION.md
Branch policy: worktree per issue; base origin/dev; never main.
Current slice: <ISSUE_ID> only. Paths: <PATHS>. Do not edit L-memory/L-ops paths.
Acceptance: tests green + scripts/check.sh --quick.
After: open PR to dev with "Closes #N".
```

## Grok kickoff blurb (self)

```text
You are L0/L-ops + L-memory for cabal-devmelopner 1.0.0.
Coordinate Claude slices; land CI; session/tero/notify; do not steal L-core files mid-slice.
Report on cabal when a phase exits.
```

---

## Exit of this plan doc

When Phase 0 issues exist on GitHub and Phase 1 first PR is open, this plan is **active**. Update checkboxes as waves complete (append-only notes at bottom).
