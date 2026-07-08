"""Prompt construction utilities for cabal-devmelopner."""

from __future__ import annotations

from typing import Sequence

from cabal_devmelopner.core.types import Task


def build_prompt(
    task: Task,
    feedback: Sequence[str] | None = None,
    extra_context: str | None = None,
) -> str:
    """
    Build a prompt for the model.

    This is a PoC version. It will be extended later to pull context from
    Tero-MCP, previous attempts, specs, etc.
    """
    parts = [f"TASK: {task.description.strip()}"]

    if extra_context:
        parts.append("\nCONTEXT:\n" + extra_context.strip())

    if feedback:
        parts.append("\nPREVIOUS ATTEMPTS AND FEEDBACK:")
        for i, fb in enumerate(feedback, 1):
            parts.append(f"\nAttempt {i} feedback:\n{fb.strip()}")

        parts.append("\nPlease fix the issues from the previous attempts and provide an improved solution.")

    parts.append("\nPlease provide a clear, well-structured response.")

    return "\n".join(parts)
