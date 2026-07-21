# Security review checklist — cabal-devmelopner 1.0

**Status:** Living checklist for E8.2. Complete before `v1.0.0` tag.  
**Date opened:** 2026-07-21

## Scope

Leaf coding agent: CLI/TUI, optional Tero client, ToolHost (fs + allowlisted commands),
config-as-code. **Not** a multi-tenant SaaS; threat model is **local developer workstation +
self-hosted CI**.

## Checklist

### Secrets & credentials

| Check | Status | Notes |
|-------|--------|-------|
| API keys only via env (`XAI_API_KEY`, `TERO_TOKENS`, …) — never committed | ☐ | Spot-check git history / gitleaks CI |
| Tokens not placed on process argv for tools | ☐ | ToolHost uses argv for allowlisted cmds only; no secrets interpolated |
| Logs/events redact token-like strings | ☐ | Prefer not logging TERO_TOKENS / API keys at all |
| Session JSONL does not store raw provider API keys | ☐ | Events should carry task/tool metadata only |

### Filesystem confinement (ToolHost)

| Check | Status | Notes |
|-------|--------|-------|
| `read_file` / `write_file` / `apply_patch` / `list_dir` confined to workspace_root | ☐ | Unit + property tests (E8.1) |
| Path escape via `..`, absolute paths, symlink tricks blocked | ☐ | |
| Writes under `.git/` refused | ☐ | |
| Write size capped (`max_write_bytes`) | ☐ | |

### Command execution

| Check | Status | Notes |
|-------|--------|-------|
| `run_command` / verify: allowlist on basename, no shell | ☐ | `shell=False`, metachar block |
| Config allowlist cannot be empty-open by accident | ☐ | Default SAFE_COMMANDS / config list |
| Verify command uses same allowlist as tools | ☐ | E2 path |

### Network & providers

| Check | Status | Notes |
|-------|--------|-------|
| Local-ollama default; frontier only with explicit key | ☐ | |
| No automatic third-party installs from agent | ☐ | No mycelium auto-clone |

### Supply chain / CI

| Check | Status | Notes |
|-------|--------|-------|
| gitleaks + trivy on PRs | ☐ | fleet-security |
| Lockfile committed (`uv.lock`) | ☐ | |
| Self-hosted runners only for trusted repos | ☐ | |

## Spot-check procedure

```bash
./scripts/check.sh --quick
rg -n 'XAI_API_KEY|TERO_TOKENS|api_key|password' src tests --glob '!**/__pycache__/**'
uv run pytest -q tests/ -k 'confinement or allowlist or escape or write_file'
```

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Implementer | | | |
| Reviewer | | | |

When all boxes are ☑ and tests green, E8.2 is complete for 1.0 ship.
