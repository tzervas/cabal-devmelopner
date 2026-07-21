"""Basic smoke tests for cabal-devmelopner PoC (expanded for A3)."""

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.events import EventBus, EventType
from cabal_devmelopner.core.tools import ToolHost, parse_tool_call
from cabal_devmelopner.core.types import Task
from cabal_devmelopner.providers.base import Provider


class MockProvider(Provider):
    """Simple mock provider for testing."""

    def __init__(self, response: str = "Mock response"):
        self.response = response
        self.call_count = 0

    def complete(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        return self.response

    def name(self) -> str:
        return "MockProvider"


def test_simple_agent_runs_once():
    """Basic smoke test that the agent can run a task."""
    provider = MockProvider(response="Test output")
    agent = SimpleAgent(provider=provider)

    task = Task(
        id="smoke-1",
        description="Test task",
        max_iterations=1,
    )

    result = agent.run(task)

    assert result == "Test output"
    assert provider.call_count == 1


def test_simple_agent_with_multiple_iterations():
    """Test that the agent respects max_iterations."""
    provider = MockProvider(response="Attempt output")
    agent = SimpleAgent(provider=provider)

    task = Task(
        id="smoke-2",
        description="Multi-iteration test",
        max_iterations=3,
    )

    result = agent.run(task)

    # With current PoC logic it returns on first success,
    # but we still want to ensure it doesn't crash with higher max_iterations.
    assert result == "Attempt output"


def test_eventbus_emits_and_subscribes():
    """A3: basic EventBus coverage (POC-7)."""
    bus = EventBus()
    seen = []

    def handler(ev):
        seen.append(ev.type)

    bus.subscribe(EventType.PROGRESS, handler)
    bus.emit_simple(EventType.PROGRESS, message="hi")
    assert EventType.PROGRESS in seen


def test_task_dataclass():
    """A3: Task is real dataclass not duck (ties to A1 POC-3)."""
    t = Task(id="t1", description="desc", max_iterations=2)
    assert t.id == "t1"
    assert t.max_iterations == 2
    assert isinstance(t.context, dict)


class FailingTeroClient:
    """Mock for Tero error path test."""

    def text_search_structured(self, query: str, limit: int = 5):
        raise RuntimeError("simulated tero mcp fail")


def test_tero_error_emits_event():
    """A3/A2: facade/tero failures surface via ERROR event (never silent), no pass-through to refusal only (C0/POC-4).
    Facade returns explicit refusal (its contract) but agent always emits ERROR for observability.
    """
    provider = MockProvider("ok")
    bus = EventBus()
    errors = []

    def on_err(ev):
        errors.append(ev.payload)

    bus.subscribe(EventType.ERROR, on_err)
    agent = SimpleAgent(provider=provider, event_bus=bus, tero_client=FailingTeroClient())

    task = Task(id="e1", description="task with tero", max_iterations=1)
    _ = agent.run(task)

    assert len(errors) >= 1
    err_str = str(errors[0].get("error", ""))
    assert "CommonMemory facade error" in err_str or "facade query failed" in err_str


def test_provider_error_emits_and_refusal():
    """A3/A2: provider failures emit ERROR + return refusal (POC-8)."""

    class BoomProvider(Provider):
        def complete(self, prompt: str, **kwargs):
            raise ValueError("boom provider")

        def name(self):
            return "Boom"

    bus = EventBus()
    errs = []
    bus.subscribe(EventType.ERROR, lambda e: errs.append(e.payload))
    agent = SimpleAgent(provider=BoomProvider(), event_bus=bus)

    task = Task(id="e2", description="will fail", max_iterations=1)
    resp = agent.run_structured(task)

    assert len(errs) >= 1
    assert "Provider error" in str(errs[0].get("error", ""))
    assert resp.kind == "refusal"
    assert "Provider failed" in resp.answer


# --- MVP-1 tools tests (B1/B2 start) ---


def test_parse_tool_call_basic():
    """MVP-1: parser recognizes the call tool ... with ... is ... format."""
    tc = parse_tool_call("call tool read_file with path is src/cabal_devmelopner/core/agent.py")
    assert tc is not None
    assert tc.name == "read_file"
    assert tc.args.get("path") == "src/cabal_devmelopner/core/agent.py"

    tc2 = parse_tool_call("call tool list_dir with path is .")
    assert tc2 and tc2.name == "list_dir"

    tc3 = parse_tool_call("I will call tool run_command with command is python -m pytest -q")
    assert tc3 and tc3.name == "run_command"


def test_tool_host_read_list_local(tmp_path, monkeypatch):
    """MVP-1: ToolHost confined to root, emits events, read/list work on real files."""
    bus = EventBus()
    calls = []
    results = []
    bus.subscribe(EventType.TOOL_CALL, lambda e: calls.append(e.payload))
    bus.subscribe(EventType.TOOL_RESULT, lambda e: results.append(e.payload))

    # write a temp file under tmp as workspace
    f = tmp_path / "README.md"
    f.write_text("hello tools\nline2")
    host = ToolHost(event_bus=bus, workspace_root=str(tmp_path))

    out = host.read_file("README.md")
    assert "hello tools" in out
    assert len(calls) >= 1 and calls[-1]["name"] == "read_file"
    assert len(results) >= 1 and results[-1]["success"] is True

    outd = host.list_dir(".")
    assert "f/README.md" in outd or "README.md" in outd  # our format has f/
    assert any(r["name"] == "list_dir" for r in results)


def test_tool_host_run_allowlisted_and_blocks():
    """MVP-1: run_command allowlist + blocks unsafe; emits."""
    bus = EventBus()
    host = ToolHost(event_bus=bus, workspace_root=".")
    res = host.run_command("echo MVP-1-safe")
    assert "MVP-1-safe" in res
    bad = host.run_command("rm -rf /")
    assert "not in allowlist" in bad or "unsafe" in bad


class ToolUsingMockProvider(Provider):
    """Mock that returns a tool call first, then a final answer on 2nd call."""

    def __init__(self):
        self.call_count = 0

    def complete(self, prompt: str, **kwargs):
        self.call_count += 1
        if self.call_count == 1:
            return "call tool list_dir with path is ."
        return "Final answer after tool: done."

    def name(self):
        return "ToolMock"


def test_agent_tools_loop_emits_and_reprompts():
    """MVP-1 basic: agent with tools_enabled parses, executes via host, emits TOOL_*, re-prompts, returns final."""
    bus = EventBus()
    tool_calls = []
    tool_results = []
    bus.subscribe(EventType.TOOL_CALL, lambda e: tool_calls.append(e.payload.get("name")))
    bus.subscribe(EventType.TOOL_RESULT, lambda e: tool_results.append(e.payload.get("name")))

    provider = ToolUsingMockProvider()
    agent = SimpleAgent(
        provider=provider,
        event_bus=bus,
        tools_enabled=True,
        workspace_root=".",
    )
    task = Task(id="tool-1", description="list files then conclude", max_iterations=3)
    resp = agent.run_structured(task)

    assert provider.call_count >= 2  # tool + final
    assert "list_dir" in tool_calls
    assert "list_dir" in tool_results
    assert resp.kind == "answer"
    assert "done" in resp.answer or "Final" in resp.answer


def test_write_file_confined(tmp_path, monkeypatch):
    from cabal_devmelopner.core.tools import ToolHost

    host = ToolHost(workspace_root=tmp_path)
    out = host.write_file("hello.txt", "world\n")
    assert "wrote" in out
    assert (tmp_path / "hello.txt").read_text() == "world\n"
    bad = host.write_file("../escape.txt", "nope")
    assert bad.startswith("[write_file error]")
    bad2 = host.write_file(".git/config", "x")
    assert "not allowed" in bad2


def test_apply_patch_unique(tmp_path):
    from cabal_devmelopner.core.tools import ToolHost

    f = tmp_path / "a.py"
    f.write_text("def foo():\n    return 1\n")
    host = ToolHost(workspace_root=tmp_path)
    out = host.apply_patch("a.py", "return 1", "return 2")
    assert "patched" in out
    assert "return 2" in f.read_text()
    # non-unique fails
    f.write_text("x = 1\ny = 1\n")
    out2 = host.apply_patch("a.py", "1", "9")
    assert out2.startswith("[apply_patch error]")


def test_parse_write_and_patch():
    from cabal_devmelopner.core.tools import parse_tool_call

    tc = parse_tool_call("call tool write_file with path is src/x.py content is print(1)")
    assert tc is not None
    assert tc.name == "write_file"
    assert tc.args.get("path") == "src/x.py"
    assert "print(1)" in tc.args.get("content", "")
    tc2 = parse_tool_call("call tool apply_patch with path is a.py old is foo new is bar")
    assert tc2 is not None
    assert tc2.name == "apply_patch"
    assert tc2.args.get("old") == "foo"
    assert tc2.args.get("new") == "bar"


# --- E2 verify loop + E3.1 budgets ---


class VerifyThenAnswerProvider(Provider):
    """First call: final answer (triggers verify). Later calls: final answers after feedback."""

    def __init__(self, answers: list[str] | None = None):
        self.call_count = 0
        self.answers = answers or ["I am done.", "Fixed. Done again."]

    def complete(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        idx = min(self.call_count - 1, len(self.answers) - 1)
        return self.answers[idx]

    def name(self) -> str:
        return "VerifyMock"


def test_verify_success_emits_and_annotates(tmp_path):
    """E2: successful verify_command emits VERIFY_* and sets extended.verify.ok."""
    bus = EventBus()
    started = []
    results = []
    bus.subscribe(EventType.VERIFY_STARTED, lambda e: started.append(e.payload))
    bus.subscribe(EventType.VERIFY_RESULT, lambda e: results.append(e.payload))

    agent = SimpleAgent(
        provider=VerifyThenAnswerProvider(["all good"]),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        verify_command="echo verify-ok",
        max_verify_rounds=1,
        use_verify=True,
        command_allowlist=("echo", "ls"),
    )
    resp = agent.run_structured(Task(id="v1", description="finish cleanly", max_iterations=3))
    assert len(started) == 1
    assert len(results) == 1
    assert results[0].get("success") is True
    assert resp.extended and resp.extended.get("verify", {}).get("ok") is True
    assert "verify-ok" in str(resp.extended.get("verify", {}).get("output", ""))


def test_verify_fail_reprompts_then_passes(tmp_path):
    """E2: failing verify re-prompts; second pass succeeds within max_verify_rounds."""
    bus = EventBus()
    results = []
    bus.subscribe(EventType.VERIFY_RESULT, lambda e: results.append(e.payload.get("success")))

    # Use a small script that fails once then passes via a marker file
    script = tmp_path / "check.sh"
    marker = tmp_path / "pass.marker"
    script.write_text(
        "#!/bin/sh\n"
        f"if [ -f '{marker}' ]; then echo PASS; exit 0; fi\n"
        f"touch '{marker}'\n"
        "echo FAIL first; exit 1\n"
    )
    script.chmod(0o755)

    provider = VerifyThenAnswerProvider(["done attempt1", "done attempt2"])
    agent = SimpleAgent(
        provider=provider,
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        verify_command="bash check.sh",
        max_verify_rounds=2,
        use_verify=True,
        command_allowlist=("bash", "sh", "echo"),
        max_tool_steps=3,
    )
    resp = agent.run_structured(
        Task(id="v2", description="repair after verify fail", max_iterations=5)
    )
    assert False in results  # at least one fail
    assert True in results  # then pass
    assert resp.extended and resp.extended.get("verify", {}).get("ok") is True
    assert provider.call_count >= 2


def test_verify_exhausted_rounds_emits_error(tmp_path):
    """E2: after max_verify_rounds failures, task finishes with verify FAILED annotation."""
    bus = EventBus()
    errors = []
    bus.subscribe(EventType.ERROR, lambda e: errors.append(e.payload))

    agent = SimpleAgent(
        provider=VerifyThenAnswerProvider(["still broken"] * 5),
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        verify_command="bash -c 'exit 1'",
        max_verify_rounds=1,
        use_verify=True,
        command_allowlist=("bash", "sh"),
    )
    # Note: bash -c may be blocked by is_safe_command if path rules fail;
    # use a failing script instead for determinism.
    fail = tmp_path / "always_fail.sh"
    fail.write_text("#!/bin/sh\necho always-fail\nexit 1\n")
    fail.chmod(0o755)
    agent.verify_command = "bash always_fail.sh"

    resp = agent.run_structured(Task(id="v3", description="cannot fix", max_iterations=6))
    assert any("verify failed" in str(e.get("error", "")).lower() for e in errors)
    assert "verify FAILED" in resp.answer
    assert resp.extended and resp.extended.get("verify", {}).get("ok") is False


def test_max_tool_steps_from_ctor(tmp_path):
    """E3.1: max_tool_steps is honored (not hardcoded)."""

    class AlwaysToolProvider(Provider):
        def __init__(self):
            self.call_count = 0
            self.saw_budget = False

        def complete(self, prompt: str, **kwargs) -> str:
            self.call_count += 1
            if "Tool step budget exceeded" in prompt:
                self.saw_budget = True
                return "Forced final after budget."
            return "call tool list_dir with path is ."

        def name(self) -> str:
            return "AlwaysTool"

    bus = EventBus()
    provider = AlwaysToolProvider()
    agent = SimpleAgent(
        provider=provider,
        event_bus=bus,
        tools_enabled=True,
        workspace_root=str(tmp_path),
        max_tool_steps=2,
        use_verify=False,
    )
    resp = agent.run_structured(Task(id="budget", description="list forever", max_iterations=8))
    # 2 successful tools + 1 budget rejection re-prompt + final
    assert provider.call_count >= 3
    assert provider.saw_budget is True
    assert "Forced final" in resp.answer or resp.kind == "answer"


def test_is_safe_command_allowlist():
    from cabal_devmelopner.core.tools import is_safe_command

    assert is_safe_command("echo hi", {"echo"})
    assert not is_safe_command("echo hi", {"pytest"})
    assert is_safe_command("uv run pytest -q", {"uv", "pytest"})
    # shell metacharacters always blocked even if basename is allowlisted
    assert not is_safe_command("echo hi; rm -rf /", {"echo"})
    assert not is_safe_command("echo hi && true", {"echo"})
    assert not is_safe_command("cat $(whoami)", {"cat"})
    # unlisted basename blocked
    assert not is_safe_command("rm -rf /tmp/x", {"echo", "pytest"})
