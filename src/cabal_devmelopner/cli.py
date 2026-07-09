"""Basic CLI for cabal-devmelopner (PoC)."""

from __future__ import annotations

import argparse
import os
import sys

from cabal_devmelopner.core.agent import SimpleAgent
from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import EventType, Task
from cabal_devmelopner.mcp.tero_client import TeroMCPClient
from cabal_devmelopner.providers.xai import XaiProvider


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cabal-devmelopner",
        description="cabal-devmelopner — Development Agent (PoC)",
        epilog="Example: cabal-devmelopner 'Improve error handling in the compiler' --use-tero",
    )
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument("--model", default="grok-4.5", help="xAI model to use")
    parser.add_argument("--use-tero", action="store_true", help="Enable Tero-MCP context retrieval")
    args = parser.parse_args()

    if not args.task:
        parser.print_help()
        sys.exit(1)

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY is not set. Please export it first.")
        sys.exit(1)

    provider = XaiProvider(api_key=api_key, model=args.model)
    event_bus = EventBus()

    # Simple event handlers for CLI output
    def on_progress(event):
        print(f"[Progress] {event.payload.get('message', '')}")

    def on_generation_complete(event):
        print(f"[Generation] Completed ({event.payload.get('response_length', 0)} chars)")

    event_bus.subscribe(EventType.PROGRESS, on_progress)
    event_bus.subscribe(EventType.GENERATION_COMPLETE, on_generation_complete)

    tero_client = TeroMCPClient() if args.use_tero else None
    agent = SimpleAgent(provider=provider, event_bus=event_bus, tero_client=tero_client)

    task = Task(
        id="cli-task-1",
        description=args.task,
        max_iterations=3,
    )

    print(f"Running task with {provider.name()}...\n")
    result = agent.run(task)
    print("\n--- Result ---")
    print(result)


if __name__ == "__main__":
    main()
