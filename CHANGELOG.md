# Changelog

All notable changes to **cabal-devmelopner** are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/).

## [Unreleased]

### Added

- **E2 verify loop:** after a tools-path final answer, run configurable
  `tools.verify_command` (default `uv run pytest -q`), emit
  `VERIFY_STARTED` / `VERIFY_RESULT`, re-prompt up to `max_verify_rounds` on
  failure, then annotate / ERROR if still red.
- **E3.1 config budgets:** `max_tool_steps`, `max_iterations`, `use_verify`,
  allowlist, and verify settings from `CabalConfig` → `SimpleAgent` / CLI
  (`--use-verify`, `--verify-command`); not hardcoded.
- Configurable `ToolHost` command allowlist + `is_safe_command` public helper.

## [0.1.0] — 2026-07-16

### Added

- **Config-as-code:** `cabal.example.toml` with **L0** (frontier) and **L1** (composer)
  profiles; loader in `core/config.py` (CLI flags > env > file > defaults).
- **CLI:** `--config`, `--profile {l0,l1}`, `--version`, `--workspace`,
  `--use-tero` / `--no-use-tero`, `--use-tools` / `--no-use-tools`.
- **CLAUDE.md** — coding-assistant surface for this product.
- **docs/COMPOSE.md** — compose with tz-forge `agent-swarm`, agent-harness,
  tg-agent-relay, optional tero-mcp (no mycelium automation).
- **CHANGELOG.md** / explicit **0.1.0** alpha release notes.
- Tests for config parse, profiles, and CLI override precedence.

### Product status (honest)

- Alpha / PoC→MVP scaffold: EventBus, xAI + local-ollama providers, optional
  Tero client + W2 CommonMemory facade, MVP-1 tools + write/apply_patch + verify loop,
  Textual TUI entrypoint.
- Not yet: streaming, multi-agent swarms, security wrappers,
  zero-config Tero, production packaging.

### Notes

- Fleet standards (P26): self-hosted CI badges, issue close on **main** only.
- Tero is opt-in sibling; mycelium is handoff-only.

[0.1.0]: https://github.com/tzervas/cabal-devmelopner/releases/tag/v0.1.0
