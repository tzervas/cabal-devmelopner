# Changelog

All notable changes to **cabal-devmelopner** are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/).

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
  Tero client + W2 CommonMemory facade, MVP-1 tools loop, Textual TUI entrypoint.
- Not yet: full verification loop, multi-agent swarms, security wrappers,
  zero-config Tero, production packaging.

### Notes

- Fleet standards (P26): self-hosted CI badges, issue close on **main** only.
- Tero is opt-in sibling; mycelium is handoff-only.

[0.1.0]: https://github.com/tzervas/cabal-devmelopner/releases/tag/v0.1.0
