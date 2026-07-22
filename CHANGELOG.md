# Changelog

All notable changes to **cabal-devmelopner** are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Planned toward 1.0.0

- Token soft budgets (beyond wall-clock)
- E8 log redaction + reviewer security sign-off
- Auto `v1.0.0` tag when RELEASE_1_0_0 bar fully met

## [0.3.0] — 2026-07-21

### Added
- **E6.2 cancel:** `SimpleAgent.request_cancel()` cooperative stop; TUI **Cancel** button.
- **E7.3 HITL writes:** `[tools] require_write_approval` / `--require-write-approval` /
  `CABAL_REQUIRE_WRITE_APPROVAL`; emits `NEEDS_HUMAN_INPUT`; CLI stdin or `CABAL_HITL_AUTO`.
- Tests: `tests/test_cancel_hitl.py`.

### Changed
- Version **0.2.1 → 0.3.0** (minor: cancel + HITL toward 1.0 bar).
- 1.0.0 may auto-tag when RELEASE_1_0_0 checklist fully met (security sign-off remaining).

## [0.2.1] — 2026-07-21

Patch release: outbound Telegram notify + soft wall-clock budget (merged from #36).

### Added

- **E7.1 notify:** `cabal_devmelopner.notify.RelayNotifier` calls tg-agent-relay
  `relay-notify.sh` (opt-in). Config `[notify]`, env `CABAL_NOTIFY` /
  `CABAL_RELAY_NOTIFY`, CLI `--notify`. Soft-fail on missing relay.
- **E3.2 soft wall budget:** `max_wall_secs` (config / `CABAL_MAX_WALL_SECS` /
  `--max-wall-secs`) stops the agent loop with ERROR `source=budget`.
- COMPOSE: inbound Telegram is platform `tg-poll` + FIFO keepalives — **no
  per-session Grok monitor** required for intake.

### Changed

- `cabal.example.toml` documents `[notify]` and wall budget knobs.

## [0.2.0] — 2026-07-21

Interim **leaf agent** release: act + verify + session + stream + TUI dogfood.
**Not** multi-agent production; **not** legitimate RAG via context-mcp.

### Added

- **Tools write path:** `write_file` / `apply_patch` workspace-confined (E1.1)
- **Tool protocol:** fenced/bare JSON `{name,args}` plus legacy free-text (E1.2)
- **Multi-step tools loop** with configurable `max_tool_steps` (E1.3 / E3.1)
- **E2 verify loop:** `tools.verify_command`, re-prompt up to `max_verify_rounds`,
  `VERIFY_STARTED` / `VERIFY_RESULT` events
- **E3.1 config budgets:** `max_tool_steps`, `max_iterations`, allowlist, `use_verify`
  from `CabalConfig` / CLI (`--use-verify`, `--verify-command`)
- **E4.1 streaming:** `Provider.complete_stream`; Ollama NDJSON; CLI `--stream`
- **E5.3 session JSONL:** `.cabal/runs/<task_id>.jsonl` via `SessionRecorder`
- **E5.1 tero errors:** actionable ERROR hints (`TERO_INDEX_PATH`, sibling layout,
  `docs/TERO.md`)
- **E6.1 TUI:** live tools/verify/error log; config-driven provider; session path
- **E8.1** path confinement property tests
- **Docs:** gap analysis, joint execution, RELEASE/SECURITY checklists, tooling readiness

### Changed

- README honesty for 0.2.0 feature set
- Default CLI description no longer claims bare alpha-only tools

### Product status (honest)

| Area | 0.2.0 |
|------|-------|
| Act (read/list/write/patch/run allowlist) | yes |
| Verify loop | yes |
| Session JSONL | yes |
| Stream (Ollama) | yes |
| Tero opt-in L1 | yes (sibling required) |
| TUI dogfood | yes |
| Notify (Telegram) | **no** (E7) |
| Wall-clock budgets | **no** (E3.2) |
| Multi-agent swarm | **no** (post-1.0) |
| Legitimate RAG | **no** (context-mcp Wave 2+) |

## [0.1.0] — 2026-07-16

### Added

- **Config-as-code:** `cabal.example.toml` with **L0** / **L1** profiles
- **CLI:** `--config`, `--profile`, `--version`, `--workspace`, `--use-tero`, `--use-tools`
- **CLAUDE.md**, **docs/COMPOSE.md**, CHANGELOG, basic tests
- EventBus, xAI + local-ollama providers, optional Tero client, MVP-1 tools, Textual TUI entry

[Unreleased]: https://github.com/tzervas/cabal-devmelopner/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/tzervas/cabal-devmelopner/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/tzervas/cabal-devmelopner/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/tzervas/cabal-devmelopner/releases/tag/v0.1.0
