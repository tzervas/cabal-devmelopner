"""Basic CLI for cabal-devmelopner (PoC + config-as-code)."""

from __future__ import annotations

import argparse
import os
import sys

from cabal_devmelopner import __version__
from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.config import load_config, merge_cli_overrides
from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.schemas import StructuredResponse
from cabal_devmelopner.core.session import SessionRecorder
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.notify import build_notifier
from cabal_devmelopner.providers.base import LocalOllamaProvider, Provider
from cabal_devmelopner.providers.xai import XaiProvider


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cabal-devmelopner",
        description="cabal-devmelopner — Development Agent (alpha)",
        epilog=(
            "Example: cabal-devmelopner 'Improve error handling' --use-tero\n"
            "Config:  copy cabal.example.toml → cabal.toml (see docs)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to cabal.toml (default: search upward for cabal.toml / .cabal-devmelopner.toml)",
    )
    parser.add_argument(
        "--profile",
        choices=["l0", "l1"],
        default=None,
        help="Config profile: l1 composer (default) or l0 frontier",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (xai default: grok-4.5; local default from --local-model / config)",
    )
    parser.add_argument(
        "--provider",
        choices=["xai", "local-ollama"],
        default=None,
        help="Provider: local-ollama (default) or xai",
    )
    parser.add_argument(
        "--local-model",
        default=None,
        help="Model for local-ollama (e.g. qwen2.5-coder:7b). Ensure pulled in Ollama.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temp (lower for coding/reliable)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Max completion tokens (keep modest for local context)",
    )
    parser.add_argument(
        "--use-tero",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable Tero-MCP context retrieval (optional sibling; see docs/TERO.md)",
    )
    parser.add_argument(
        "--use-tools",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable MVP-1 minimal tools (read_file, list_dir, run_command allowlisted)",
    )
    parser.add_argument(
        "--use-verify",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="After tools final answer, run tools.verify_command and re-prompt on failure (E2)",
    )
    parser.add_argument(
        "--verify-command",
        default=None,
        help="Override [tools].verify_command (e.g. 'uv run pytest -q')",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Workspace root (default: config project.workspace_root or .)",
    )
    parser.add_argument(
        "--structured",
        action="store_true",
        default=True,
        help="Use StructuredResponse path (W2 schemas, citations, orchestration hints)",
    )
    parser.add_argument(
        "--stream",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Stream provider tokens to stdout when available (E4.1; default on)",
    )
    parser.add_argument(
        "--notify",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Outbound Telegram status via tg-agent-relay (E7.1; needs relay-notify.sh)",
    )
    parser.add_argument(
        "--max-wall-secs",
        type=float,
        default=None,
        help="Soft wall-clock budget seconds (E3.2; 0 disables)",
    )
    parser.add_argument(
        "--require-write-approval",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="E7.3 HITL: require approval before write_file/apply_patch",
    )
    args = parser.parse_args()

    if not args.task:
        parser.print_help()
        sys.exit(1)

    base = load_config(args.config) if args.config else load_config()
    cfg = merge_cli_overrides(
        base,
        provider=args.provider,
        model=args.model,
        local_model=args.local_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        use_tero=args.use_tero,
        use_tools=args.use_tools,
        use_verify=args.use_verify,
        profile=args.profile,
        workspace_root=args.workspace,
        verify_command=args.verify_command,
    )
    # CLI notify / wall budget (highest precedence)
    from dataclasses import replace as _replace

    if args.notify is not None:
        cfg = _replace(cfg, notify=_replace(cfg.notify, enabled=args.notify))
    if args.max_wall_secs is not None:
        wall = None if args.max_wall_secs <= 0 else float(args.max_wall_secs)
        cfg = _replace(cfg, max_wall_secs=wall)
    if args.require_write_approval is not None:
        cfg = _replace(
            cfg,
            tools=_replace(cfg.tools, require_write_approval=args.require_write_approval),
        )

    provider_name = cfg.profile.provider
    model = cfg.profile.model
    temperature = cfg.profile.temperature
    max_tokens = cfg.profile.max_tokens
    local_model = cfg.profile.local_model
    provider: Provider

    if provider_name == "xai":
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            print("Error: XAI_API_KEY not set. Falling back to local-ollama (self-hosted).")
            provider_name = "local-ollama"
        else:
            model = model or "grok-4.5"
            provider = XaiProvider(api_key=api_key, model=model)
    if provider_name == "local-ollama":
        model = model or local_model
        provider = LocalOllamaProvider(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        print(
            f"Using LOCAL self-hosted provider: {provider.name()} "
            f"(profile={cfg.profile.name}). Ollama must be up (http://localhost:11434)."
        )
    event_bus = EventBus()

    def on_progress(event):  # type: ignore[no-untyped-def]
        print(f"[Progress] {event.payload.get('message', '')}")

    def on_generation_complete(event):  # type: ignore[no-untyped-def]
        print(f"[Generation] Completed ({event.payload.get('response_length', 0)} chars)")

    event_bus.subscribe(EventType.PROGRESS, on_progress)
    event_bus.subscribe(EventType.GENERATION_COMPLETE, on_generation_complete)

    def on_error(event):  # type: ignore[no-untyped-def]
        print(
            f"[ERROR] {event.payload.get('error', '')} (source={event.payload.get('source', '?')})"
        )

    def on_task_started(event):  # type: ignore[no-untyped-def]
        print(f"[Task] {event.payload.get('description', '')} (id={event.payload.get('task_id')})")

    event_bus.subscribe(EventType.ERROR, on_error)
    event_bus.subscribe(EventType.TASK_STARTED, on_task_started)

    def on_tool_call(event):  # type: ignore[no-untyped-def]
        print(f"[TOOL_CALL] {event.payload.get('name')} args={event.payload.get('args')}")

    def on_tool_result(event):  # type: ignore[no-untyped-def]
        out = str(event.payload.get("output", ""))[:200]
        print(
            f"[TOOL_RESULT] {event.payload.get('name')} success={event.payload.get('success')}: {out}..."
        )

    event_bus.subscribe(EventType.TOOL_CALL, on_tool_call)
    event_bus.subscribe(EventType.TOOL_RESULT, on_tool_result)

    def on_verify_started(event):  # type: ignore[no-untyped-def]
        print(
            f"[VERIFY] start: {event.payload.get('command')} "
            f"(round={event.payload.get('round', 0)})"
        )

    def on_verify_result(event):  # type: ignore[no-untyped-def]
        ok = event.payload.get("success")
        out = str(event.payload.get("output", ""))[:200]
        print(f"[VERIFY] {'ok' if ok else 'FAIL'}: {out}")

    event_bus.subscribe(EventType.VERIFY_STARTED, on_verify_started)
    event_bus.subscribe(EventType.VERIFY_RESULT, on_verify_result)

    def on_needs_human(event):  # type: ignore[no-untyped-def]
        print(
            f"[HITL] needs human input: tool={event.payload.get('tool')} "
            f"reason={event.payload.get('reason')} args={event.payload.get('args')}"
        )

    event_bus.subscribe(EventType.NEEDS_HUMAN_INPUT, on_needs_human)

    def _hitl_approval(name: str, tool_args: dict) -> bool:
        """E7.3: approve writes. CABAL_HITL_AUTO=1 for CI; else stdin y/N."""
        auto = os.getenv("CABAL_HITL_AUTO", "").strip().lower()
        if auto in {"1", "true", "yes", "on"}:
            print(f"[HITL] auto-approved {name} (CABAL_HITL_AUTO)")
            return True
        if auto in {"0", "false", "no", "off", "deny"}:
            print(f"[HITL] auto-denied {name} (CABAL_HITL_AUTO)")
            return False
        if not sys.stdin.isatty():
            print(f"[HITL] non-interactive stdin — denying {name} (set CABAL_HITL_AUTO=1)")
            return False
        try:
            ans = input(f"[HITL] approve {name} {list(tool_args.keys())}? [y/N] ").strip().lower()
        except EOFError:
            return False
        return ans in {"y", "yes"}

    # Apply optional tero path env from config (no mycelium automation)
    if cfg.tero.mcp_project:
        os.environ.setdefault("TERO_MCP_PROJECT", cfg.tero.mcp_project)
    if cfg.tero.index_path:
        os.environ.setdefault("TERO_INDEX_PATH", cfg.tero.index_path)
    if cfg.tero.tokens:
        os.environ.setdefault("TERO_TOKENS", cfg.tero.tokens)
    if cfg.tero.token:
        os.environ.setdefault("TERO_TOKEN", cfg.tero.token)

    tero_client = TeroMCPClient() if cfg.profile.use_tero else None
    notifier, notify_flags = build_notifier(
        enabled=cfg.notify.enabled,
        script=cfg.notify.relay_script,
        event_bus=event_bus,
        on_complete=cfg.notify.on_complete,
        on_error=cfg.notify.on_error,
    )
    # E3.1/E3.2: budgets + allowlist + E2 verify from CabalConfig
    agent = SimpleAgent(
        provider=provider,
        event_bus=event_bus,
        tero_client=tero_client,
        tools_enabled=cfg.use_tools,
        workspace_root=cfg.workspace_root,
        max_tool_steps=cfg.max_tool_steps,
        verify_command=cfg.tools.verify_command if cfg.use_verify else None,
        max_verify_rounds=cfg.tools.max_verify_rounds,
        use_verify=cfg.use_verify and cfg.use_tools,
        command_allowlist=cfg.tools.allowlist,
        max_wall_secs=cfg.max_wall_secs,
        require_write_approval=cfg.tools.require_write_approval,
        approval_callback=_hitl_approval if cfg.tools.require_write_approval else None,
    )

    task = Task(
        id="cli-task-1",
        description=args.task,
        max_iterations=cfg.max_iterations,
    )

    # E5.3: record the full run (events + final answer) to .cabal/runs/<task_id>.jsonl
    recorder = SessionRecorder(cfg.workspace_root, task.id)
    recorder.attach(event_bus)

    tools_note = " +tools" if cfg.use_tools else ""
    verify_note = (
        f" +verify={cfg.tools.verify_command!r}"
        if (cfg.use_tools and cfg.use_verify and cfg.tools.verify_command)
        else ""
    )
    tero_note = " +tero" if cfg.profile.use_tero else ""
    stream_note = " +stream" if args.stream else ""
    notify_note = " +notify" if cfg.notify.enabled else ""
    wall_note = f" wall={cfg.max_wall_secs}s" if cfg.max_wall_secs else ""
    src_note = f" config={cfg.source_path}" if cfg.source_path else " config=defaults"
    print(
        f"Running task with {provider.name()}{tools_note}{verify_note}{tero_note}"
        f"{stream_note}{notify_note}{wall_note} "
        f"(profile={cfg.profile.name}{src_note})...\n"
    )

    # E4.1: optional progressive preview via provider.complete_stream (agent still uses complete)
    if args.stream and not cfg.use_tools:
        print("--- stream ---")
        try:
            for chunk in provider.complete_stream(args.task):
                print(chunk, end="", flush=True)
            print("\n--- end stream (agent structured pass follows) ---\n")
        except Exception as e:
            print(f"\n[stream error] {e}; falling back to non-stream agent path\n")

    structured: StructuredResponse = agent.run_structured(task)
    recorder.record_final(structured.to_dict())
    print(f"\n[session] recorded run → {recorder.path}")

    # E7.1 outbound status (never blocks success of the task)
    is_err = structured.kind == "refusal" or (structured.extended or {}).get("budget") is not None
    if notify_flags.get("on_error") and is_err:
        notifier.notify(
            f"task={task.id} FAIL kind={structured.kind}: {(structured.answer or '')[:200]}",
            label=cfg.notify.label,
        )
    elif notify_flags.get("on_complete"):
        notifier.notify(
            f"task={task.id} complete kind={structured.kind}: {(structured.answer or '')[:200]}",
            label=cfg.notify.label,
        )

    print("\n--- StructuredResponse (schema v1, answer + citations + optionals) ---")
    print("kind:", structured.kind)
    print("answer:", structured.answer[:800] if len(structured.answer) > 800 else structured.answer)
    if structured.citations:
        print("citations:", [f"{c.id}@{c.file}:{c.line}" for c in structured.citations[:3]])
    if structured.lang_refs:
        print("lang_refs:", structured.lang_refs)
    if structured.orchestration:
        print("orchestration:", structured.orchestration)
    print("extended keys:", list((structured.extended or {}).keys())[:5] or "none")
    print("\n--- Raw text (compat) ---")
    print(structured.answer)


if __name__ == "__main__":
    main()
