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

## Phase 0 — Bookkeeping (days 0–2) — **L-ops**

- [ ] Create GitHub milestone **v1.0.0**  
- [ ] File epic issues E0–E8 + P0 children from gap analysis  
- [ ] Close completed #2–#4, #8; retitle #5–#7  
- [ ] Merge any open fleet PRs that are green  

## Phase 1 — Act + Verify (weeks 1–3) — **L-core** primary

| Order | Issue | Owner |
|------:|-------|--------|
| 1 | E1.1 write/apply_patch | Claude |
| 2 | E1.2 structured tool protocol | Claude |
| 3 | E1.3 multi-step tools loop | Claude |
| 4 | E2.1–E2.2 verify loop | Claude |
| 5 | E3.1 config→agent budgets | Claude |
| — | Review / CI babysit | Grok |

## Phase 2 — Stream + Session + Tero (weeks 2–4, parallel) — **L-surface + L-memory**

| Issue | Owner |
|-------|--------|
| E4.1 streaming | Claude (providers) |
| E5.3 JSONL session | Grok |
| E5.1 zero-config errors | Grok |
| E6.1 TUI log/status | Claude after stream API stable |

## Phase 3 — Polish + Ship (weeks 4–7)

| Issue | Owner |
|-------|--------|
| E6.2–E6.4 TUI cancel/thread | Claude |
| E7.1 Telegram notify | Grok (tg-agent-relay) |
| E7.3 HITL | Claude |
| E3.3 packaging smoke | Grok |
| E8.* hardening + release | Joint; Grok tags |

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
