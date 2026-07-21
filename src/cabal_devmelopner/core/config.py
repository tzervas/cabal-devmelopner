"""Config-as-code loader for cabal.toml / .cabal-devmelopner.toml.

Precedence (highest wins): explicit overrides (CLI) > env > file > defaults.

Profiles:
  l1 — composer / fast implementer (default)
  l0 — frontier / hard architecture (named only)

No mycelium automation: tero paths are optional strings only.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

DEFAULT_PROFILE = "l1"
CONFIG_FILENAMES = ("cabal.toml", ".cabal-devmelopner.toml")


@dataclass(frozen=True)
class TeroConfig:
    enabled: bool = False
    mcp_project: str | None = None
    index_path: str | None = None
    tokens: str | None = None
    token: str | None = None


@dataclass(frozen=True)
class ToolsConfig:
    allowlist: tuple[str, ...] = (
        "pytest",
        "ruff",
        "mypy",
        "uv",
        "python",
        "python3",
        "ls",
        "cat",
        "head",
        "git",
        "bash",  # only for verify scripts if explicitly allowlisted
    )
    # After tools finish (or on --verify), run this command under workspace root
    verify_command: str | None = "uv run pytest -q"
    # How many times to re-prompt after a failing verify before giving up
    max_verify_rounds: int = 2


@dataclass(frozen=True)
class ProfileConfig:
    name: str = DEFAULT_PROFILE
    description: str = "Composer / fast implementer (default)"
    provider: str = "local-ollama"
    model: str | None = None
    local_model: str = "llama3.2"
    temperature: float = 0.2
    max_tokens: int = 2048
    use_tero: bool = False


@dataclass(frozen=True)
class NotifyConfig:
    """E7.1 outbound status via tg-agent-relay (optional)."""

    enabled: bool = False
    # Path to relay-notify.sh; empty → resolve well-known install / CABAL_RELAY_NOTIFY
    relay_script: str | None = None
    on_complete: bool = True
    on_error: bool = True
    label: str = "cabal"


@dataclass(frozen=True)
class CabalConfig:
    """Resolved runtime configuration."""

    project_name: str = "workspace"
    workspace_root: str = "."
    max_tool_steps: int = 5
    max_iterations: int = 5
    # E3.2: soft wall-clock budget (seconds). None / 0 = disabled.
    max_wall_secs: float | None = 900.0
    structured: bool = True
    use_tools: bool = False
    # When tools enabled, run verify_command after a final answer (E2)
    use_verify: bool = True
    profile: ProfileConfig = field(default_factory=ProfileConfig)
    tero: TeroConfig = field(default_factory=TeroConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    notify: NotifyConfig = field(default_factory=NotifyConfig)
    source_path: str | None = None


def find_config_path(start: Path | None = None) -> Path | None:
    """Walk up from start (or cwd) looking for known config filenames."""
    cur = (start or Path.cwd()).resolve()
    for directory in (cur, *cur.parents):
        for name in CONFIG_FILENAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate
        # Stop at filesystem root
        if directory.parent == directory:
            break
    return None


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _profile_from_table(name: str, table: dict[str, Any]) -> ProfileConfig:
    return ProfileConfig(
        name=name,
        description=str(table.get("description", name)),
        provider=str(table.get("provider", "local-ollama")),
        model=table.get("model"),
        local_model=str(table.get("local_model", "llama3.2")),
        temperature=float(table.get("temperature", 0.2)),
        max_tokens=int(table.get("max_tokens", 2048)),
        use_tero=_as_bool(table.get("use_tero"), False),
    )


def _default_profiles() -> dict[str, ProfileConfig]:
    return {
        "l1": ProfileConfig(
            name="l1",
            description="Composer / fast implementer (default)",
            provider="local-ollama",
            model="qwen2.5-coder:7b",
            local_model="qwen2.5-coder:7b",
            temperature=0.2,
            max_tokens=2048,
            use_tero=True,
        ),
        "l0": ProfileConfig(
            name="l0",
            description="Frontier (hard architecture; use sparingly)",
            provider="xai",
            model="grok-4.5",
            local_model="qwen2.5-coder:7b",
            temperature=0.2,
            max_tokens=4096,
            use_tero=True,
        ),
    }


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def parse_config_data(data: dict[str, Any], *, source_path: str | None = None) -> CabalConfig:
    """Parse a cabal.toml-shaped dict into CabalConfig."""
    project = data.get("project") or {}
    agent = data.get("agent") or {}
    tero_t = data.get("tero") or {}
    tools_t = data.get("tools") or {}
    notify_t = data.get("notify") or {}
    profiles_raw = data.get("profiles") or {}

    profiles = _default_profiles()
    if isinstance(profiles_raw, dict):
        for pname, ptable in profiles_raw.items():
            if isinstance(ptable, dict):
                profiles[str(pname).lower()] = _profile_from_table(str(pname).lower(), ptable)

    profile_name = str(agent.get("profile", DEFAULT_PROFILE)).lower()
    profile = profiles.get(profile_name, profiles[DEFAULT_PROFILE])

    allow = tools_t.get("allowlist")
    verify_cmd = tools_t.get("verify_command")
    max_vr = tools_t.get("max_verify_rounds")
    if isinstance(allow, list) and allow:
        tools = ToolsConfig(
            allowlist=tuple(str(x) for x in allow),
            verify_command=(
                str(verify_cmd) if verify_cmd is not None else ToolsConfig().verify_command
            ),
            max_verify_rounds=int(max_vr) if max_vr is not None else 2,
        )
    else:
        tools = ToolsConfig(
            verify_command=(
                str(verify_cmd) if verify_cmd is not None else ToolsConfig().verify_command
            ),
            max_verify_rounds=int(max_vr) if max_vr is not None else 2,
        )
    if verify_cmd is not None and str(verify_cmd).strip() == "":
        tools = replace(tools, verify_command=None)

    tero = TeroConfig(
        enabled=_as_bool(tero_t.get("enabled"), False),
        mcp_project=tero_t.get("mcp_project"),
        index_path=tero_t.get("index_path"),
        tokens=tero_t.get("tokens"),
        token=tero_t.get("token"),
    )

    # Profile use_tero OR [tero].enabled can enable tero; profile is primary hint
    use_tero = profile.use_tero or tero.enabled

    wall = agent.get("max_wall_secs")
    max_wall: float | None
    if wall is None:
        max_wall = 900.0
    elif wall == "" or wall is False:
        max_wall = None
    else:
        max_wall = float(wall)
        if max_wall <= 0:
            max_wall = None

    notify = NotifyConfig(
        enabled=_as_bool(notify_t.get("enabled"), False),
        relay_script=(str(notify_t["relay_script"]) if notify_t.get("relay_script") else None),
        on_complete=_as_bool(notify_t.get("on_complete"), True),
        on_error=_as_bool(notify_t.get("on_error"), True),
        label=str(notify_t.get("label", "cabal")),
    )

    return CabalConfig(
        project_name=str(project.get("name", "workspace")),
        workspace_root=str(project.get("workspace_root", ".")),
        max_tool_steps=int(agent.get("max_tool_steps", 5)),
        max_iterations=int(agent.get("max_iterations", 5)),
        max_wall_secs=max_wall,
        structured=_as_bool(agent.get("structured"), True),
        use_tools=_as_bool(agent.get("use_tools"), False),
        use_verify=_as_bool(agent.get("use_verify"), True),
        profile=replace(profile, use_tero=use_tero),
        tero=replace(tero, enabled=use_tero),
        tools=tools,
        notify=notify,
        source_path=source_path,
    )


def apply_env(cfg: CabalConfig) -> CabalConfig:
    """Apply environment overrides (middle precedence layer)."""
    profile = cfg.profile
    tero = cfg.tero

    provider = os.getenv("CABAL_PROVIDER", profile.provider)
    model = os.getenv("CABAL_MODEL", profile.model)
    local_model = os.getenv("CABAL_LOCAL_MODEL", profile.local_model)
    use_tero_env = os.getenv("USE_TERO") or os.getenv("CABAL_USE_TERO")
    use_tero = profile.use_tero
    if use_tero_env is not None:
        use_tero = _as_bool(use_tero_env, use_tero)

    profile_name = os.getenv("CABAL_PROFILE", profile.name).lower()
    if profile_name != profile.name and profile_name in _default_profiles():
        profile = _default_profiles()[profile_name]

    mcp_project = os.getenv("TERO_MCP_PROJECT", tero.mcp_project)
    index_path = os.getenv("TERO_INDEX_PATH", tero.index_path)
    tokens = os.getenv("TERO_TOKENS", tero.tokens)
    token = os.getenv("TERO_TOKEN", tero.token)

    workspace = os.getenv("CABAL_WORKSPACE_ROOT", cfg.workspace_root)

    notify = cfg.notify
    notify_en = os.getenv("CABAL_NOTIFY") or os.getenv("CABAL_USE_NOTIFY")
    if notify_en is not None:
        notify = replace(notify, enabled=_as_bool(notify_en, notify.enabled))
    relay_script = os.getenv("CABAL_RELAY_NOTIFY") or os.getenv("RELAY_NOTIFY")
    if relay_script:
        notify = replace(notify, relay_script=relay_script)

    wall_env = os.getenv("CABAL_MAX_WALL_SECS")
    max_wall = cfg.max_wall_secs
    if wall_env is not None:
        try:
            w = float(wall_env)
            max_wall = None if w <= 0 else w
        except ValueError:
            pass

    return replace(
        cfg,
        workspace_root=workspace,
        max_wall_secs=max_wall,
        notify=notify,
        profile=replace(
            profile,
            name=profile_name,
            provider=provider,
            model=model,
            local_model=local_model or profile.local_model,
            use_tero=use_tero,
        ),
        tero=replace(
            tero,
            enabled=use_tero,
            mcp_project=mcp_project,
            index_path=index_path,
            tokens=tokens,
            token=token,
        ),
    )


def load_config(
    path: Path | str | None = None,
    *,
    search: bool = True,
) -> CabalConfig:
    """Load config from an explicit path or by searching upward."""
    cfg_path: Path | None
    if path is not None:
        cfg_path = Path(path)
        if not cfg_path.is_file():
            raise FileNotFoundError(f"config not found: {cfg_path}")
    elif search:
        cfg_path = find_config_path()
    else:
        cfg_path = None

    if cfg_path is None:
        cfg = CabalConfig()
    else:
        cfg = parse_config_data(load_toml(cfg_path), source_path=str(cfg_path))

    return apply_env(cfg)


def merge_cli_overrides(
    cfg: CabalConfig,
    *,
    provider: str | None = None,
    model: str | None = None,
    local_model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    use_tero: bool | None = None,
    use_tools: bool | None = None,
    use_verify: bool | None = None,
    profile: str | None = None,
    workspace_root: str | None = None,
    verify_command: str | None = None,
) -> CabalConfig:
    """Apply CLI flag overrides (highest precedence). None means 'unset'."""
    p = cfg.profile
    if profile is not None:
        defaults = _default_profiles()
        key = profile.lower()
        p = defaults[key] if key in defaults else replace(p, name=key)

    if provider is not None:
        p = replace(p, provider=provider)
    if model is not None:
        p = replace(p, model=model)
    if local_model is not None:
        p = replace(p, local_model=local_model)
    if temperature is not None:
        p = replace(p, temperature=temperature)
    if max_tokens is not None:
        p = replace(p, max_tokens=max_tokens)
    if use_tero is not None:
        p = replace(p, use_tero=use_tero)

    tools = cfg.tools
    if verify_command is not None:
        tools = replace(tools, verify_command=verify_command if verify_command.strip() else None)

    return replace(
        cfg,
        workspace_root=workspace_root if workspace_root is not None else cfg.workspace_root,
        use_tools=use_tools if use_tools is not None else cfg.use_tools,
        use_verify=use_verify if use_verify is not None else cfg.use_verify,
        tools=tools,
        profile=p,
        tero=replace(
            cfg.tero, enabled=p.use_tero if use_tero is not None else cfg.tero.enabled or p.use_tero
        ),
    )
