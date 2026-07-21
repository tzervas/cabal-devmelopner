"""E8.1 — property-style path confinement tests for ToolHost."""

from __future__ import annotations

from pathlib import Path

import pytest

from cabal_devmelopner.core.tools import ToolHost, is_safe_command

# Paths that must never resolve inside the workspace for escape attacks
ESCAPE_PATHS = [
    "../escape.txt",
    "../../etc/passwd",
    "/etc/passwd",
    "/tmp/out.txt",
    "..",
    "../",
    "foo/../../etc/passwd",
    "sub/../../../outside",
    ".git/config",
    ".git/hooks/pre-commit",
    "nested/.git/objects/xx",
]

SAFE_RELATIVE = [
    "a.txt",
    "src/main.py",
    "docs/readme.md",
    "nested/deep/file.txt",
    "./ok.txt",
]


@pytest.fixture
def host(tmp_path: Path) -> ToolHost:
    (tmp_path / "src").mkdir()
    (tmp_path / "nested" / "deep").mkdir(parents=True)
    (tmp_path / "src" / "main.py").write_text("print(1)\n")
    return ToolHost(workspace_root=tmp_path)


@pytest.mark.parametrize("path", ESCAPE_PATHS)
def test_read_blocks_escape_paths(host: ToolHost, path: str) -> None:
    out = host.read_file(path)
    assert out.startswith("[read_file error]") or "not a file" in out or "not allowed" in out


@pytest.mark.parametrize("path", ESCAPE_PATHS)
def test_write_blocks_escape_paths(host: ToolHost, path: str) -> None:
    out = host.write_file(path, "pwned")
    assert out.startswith("[write_file error]") or "not allowed" in out


@pytest.mark.parametrize("path", ESCAPE_PATHS)
def test_apply_patch_blocks_escape_paths(host: ToolHost, path: str) -> None:
    out = host.apply_patch(path, "a", "b")
    assert out.startswith("[apply_patch error]") or "not allowed" in out


@pytest.mark.parametrize("path", SAFE_RELATIVE)
def test_write_allows_safe_relative(host: ToolHost, tmp_path: Path, path: str) -> None:
    # strip leading ./
    rel = path[2:] if path.startswith("./") else path
    out = host.write_file(rel, "ok\n")
    assert "wrote" in out, out
    assert (tmp_path / rel).is_file()


def test_resolve_never_leaves_root(host: ToolHost, tmp_path: Path) -> None:
    for path in ESCAPE_PATHS + SAFE_RELATIVE + ["", " ", "a/b/c"]:
        resolved = host._resolve_in_workspace(path)  # noqa: SLF001 — intentional unit seam
        if resolved is None:
            continue
        assert str(resolved).startswith(str(tmp_path.resolve()))


def test_list_dir_blocks_absolute(host: ToolHost) -> None:
    out = host.list_dir("/etc")
    assert out.startswith("[list_dir error]")


@pytest.mark.parametrize(
    "cmd,ok",
    [
        ("echo hi", True),
        ("pytest -q", True),
        ("uv run pytest -q", True),
        ("rm -rf /", False),  # not allowlisted
        ("echo hi; rm -rf /", False),
        ("echo hi && true", False),
        ("cat $(whoami)", False),
        ("python -c 'print(1)'", True),
    ],
)
def test_is_safe_command_matrix(cmd: str, ok: bool) -> None:
    allowed = {"echo", "pytest", "uv", "python", "python3", "cat", "ls"}
    assert is_safe_command(cmd, allowed) is ok
