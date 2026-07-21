"""Tests for config-as-code (cabal.toml profiles)."""

from __future__ import annotations

from pathlib import Path

from cabal_devmelopner.core.config import (
    DEFAULT_PROFILE,
    load_config,
    load_toml,
    merge_cli_overrides,
    parse_config_data,
)


def test_parse_example_toml():
    """cabal.example.toml must parse and expose L0/L1 profiles."""
    example = Path(__file__).resolve().parents[1] / "cabal.example.toml"
    assert example.is_file()
    data = load_toml(example)
    cfg = parse_config_data(data, source_path=str(example))
    assert cfg.profile.name == "l1"
    assert cfg.profile.provider in {"local-ollama", "xai"}
    assert cfg.profile.use_tero is True
    assert cfg.max_tool_steps >= 1
    assert "pytest" in cfg.tools.allowlist


def test_default_config_no_file(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = load_config(search=True)
    assert cfg.profile.name == DEFAULT_PROFILE
    assert cfg.source_path is None
    assert cfg.workspace_root == "."


def test_load_explicit_path(tmp_path: Path):
    path = tmp_path / "cabal.toml"
    path.write_text(
        """
[project]
name = "unit"
workspace_root = "/tmp/ws"

[agent]
profile = "l0"
use_tools = true
max_iterations = 3

[profiles.l0]
provider = "xai"
model = "grok-4.5"
use_tero = true
""",
        encoding="utf-8",
    )
    cfg = load_config(path)
    assert cfg.project_name == "unit"
    assert cfg.workspace_root == "/tmp/ws"
    assert cfg.profile.name == "l0"
    assert cfg.profile.provider == "xai"
    assert cfg.profile.model == "grok-4.5"
    assert cfg.use_tools is True
    assert cfg.max_iterations == 3
    assert cfg.source_path == str(path)


def test_cli_overrides_win():
    base = parse_config_data(
        {
            "agent": {"profile": "l1", "use_tools": False},
            "profiles": {
                "l1": {
                    "provider": "local-ollama",
                    "local_model": "llama3.2",
                    "use_tero": False,
                }
            },
        }
    )
    cfg = merge_cli_overrides(
        base,
        provider="xai",
        model="grok-4.5",
        use_tero=True,
        use_tools=True,
        profile="l0",
    )
    assert cfg.profile.name == "l0"
    assert cfg.profile.provider == "xai"
    assert cfg.profile.model == "grok-4.5"
    assert cfg.profile.use_tero is True
    assert cfg.use_tools is True


def test_no_mycelium_automation_keys_required():
    """Config must not require mycelium paths; tero is optional."""
    cfg = parse_config_data({"agent": {"profile": "l1"}})
    assert cfg.tero.mcp_project is None
    assert cfg.tero.index_path is None


def test_verify_and_budget_fields_from_toml():
    """E2/E3.1: verify_command, max_verify_rounds, use_verify, max_tool_steps wire from toml."""
    cfg = parse_config_data(
        {
            "agent": {
                "profile": "l1",
                "use_tools": True,
                "use_verify": True,
                "max_tool_steps": 7,
                "max_iterations": 4,
            },
            "tools": {
                "allowlist": ["pytest", "uv", "echo"],
                "verify_command": "uv run pytest -q",
                "max_verify_rounds": 1,
            },
        }
    )
    assert cfg.use_tools is True
    assert cfg.use_verify is True
    assert cfg.max_tool_steps == 7
    assert cfg.max_iterations == 4
    assert cfg.tools.verify_command == "uv run pytest -q"
    assert cfg.tools.max_verify_rounds == 1
    assert "echo" in cfg.tools.allowlist


def test_empty_verify_command_disables():
    """Empty verify_command string means no verify (E2 opt-out via config)."""
    cfg = parse_config_data(
        {
            "agent": {"use_verify": True},
            "tools": {"verify_command": ""},
        }
    )
    assert cfg.tools.verify_command is None


def test_cli_verify_overrides():
    base = parse_config_data(
        {
            "agent": {"use_verify": True, "use_tools": True},
            "tools": {"verify_command": "uv run pytest -q"},
        }
    )
    cfg = merge_cli_overrides(base, use_verify=False, verify_command="echo ok")
    assert cfg.use_verify is False
    assert cfg.tools.verify_command == "echo ok"
