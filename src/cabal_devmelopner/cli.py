"""Basic CLI for cabal-devmelopner (PoC)."""

from __future__ import annotations

import argparse
import os
import sys

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.schemas import StructuredResponse
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.base import LocalOllamaProvider
from cabal_devmelopner.providers.xai import XaiProvider


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cabal-devmelopner",
        description="cabal-devmelopner — Development Agent (PoC)",
        epilog="Example: cabal-devmelopner 'Improve error handling in the compiler' --use-tero",
    )
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (xai default: grok-4.5; local default from --local-model)",
    )
    parser.add_argument(
        "--provider",
        choices=["xai", "local-ollama"],
        default="local-ollama",
        help="Provider: local-ollama (default, self-hosted GPU) or xai",
    )
    parser.add_argument(
        "--local-model",
        default="llama3.2",
        help="Model for local-ollama (e.g. qwen2.5:7b, deepseek-coder:6.7b, llama3.1). Ensure pulled in Ollama.",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.2, help="Sampling temp (lower for coding/reliable)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Max completion tokens (keep modest for local context)",
    )
    parser.add_argument(
        "--use-tero",
        action="store_true",
        help="Enable Tero-MCP context retrieval (dynamic Rust surface + citations)",
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

    model = args.model
    if args.provider == "xai":
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            print("Error: XAI_API_KEY not set. Falling back to local-ollama (GPU self-hosted).")
            args.provider = "local-ollama"
        else:
            model = model or "grok-4.5"
            provider = XaiProvider(api_key=api_key, model=model)
    if args.provider == "local-ollama":
        model = model or args.local_model
        provider = LocalOllamaProvider(
            model=model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        print(
            f"Using LOCAL self-hosted provider: {provider.name()} on GPU (RTX 5080+). Ollama server must be up (http://localhost:11434). Prefer for leaves/efficient work."
        )
    event_bus = EventBus()

    # Simple event handlers for CLI output
    def on_progress(event):
        print(f"[Progress] {event.payload.get('message', '')}")

    def on_generation_complete(event):
        print(f"[Generation] Completed ({event.payload.get('response_length', 0)} chars)")

    event_bus.subscribe(EventType.PROGRESS, on_progress)
    event_bus.subscribe(EventType.GENERATION_COMPLETE, on_generation_complete)

    # A2: surface errors (POC-8); also task start for visibility
    def on_error(event):
        print(
            f"[ERROR] {event.payload.get('error', '')} (source={event.payload.get('source', '?')})"
        )

    def on_task_started(event):
        print(f"[Task] {event.payload.get('description', '')} (id={event.payload.get('task_id')})")

    event_bus.subscribe(EventType.ERROR, on_error)
    event_bus.subscribe(EventType.TASK_STARTED, on_task_started)

    tero_client = TeroMCPClient() if args.use_tero else None
    agent = SimpleAgent(provider=provider, event_bus=event_bus, tero_client=tero_client)

    task = Task(
        id="cli-task-1",
        description=args.task,
        max_iterations=3,
    )

    print(
        f"Running task with {provider.name()} (local GPU/optimizations enabled where applicable, tero for scoped cross-repo memory)...\n"
    )
    # Use structured path (applies schemas for memory + future orchestration efficiency)
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
