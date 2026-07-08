"""Base classes for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """Abstract base class for model providers (xAI, Claude, etc.)."""

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion from the given prompt."""
        ...

    @abstractmethod
    def name(self) -> str:
        """Return the name of this provider."""
        ...
