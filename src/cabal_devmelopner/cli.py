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
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
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
        profile=args.profile,
        workspace_root=args.workspace,
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
    agent = SimpleAgent(
        provider=provider,
        event_bus=event_bus,
        tero_client=tero_client,
        tools_enabled=cfg.use_tools,
        workspace_root=cfg.workspace_root,
    )

    task = Task(
        id="cli-task-1",
        description=args.task,
        max_iterations=cfg.max_iterations,
    )

    tools_note = " +tools" if cfg.use_tools else ""
    tero_note = " +tero" if cfg.profile.use_tero else ""
    src_note = f" config={cfg.source_path}" if cfg.source_path else " config=defaults"
    print(
        f"Running task with {provider.name()}{tools_note}{tero_note} "
        f"(profile={cfg.profile.name}{src_note})...\n"
    )
    structured: StructuredResponse = agent.run_structured(task)
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
