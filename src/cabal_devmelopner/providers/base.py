"""Base classes for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """Abstract base class for model providers (xAI, Claude, local llama.cpp/Ollama, etc.).

    Supports self-hosted for cost/privacy/GPU optimization in workspace vision.
    """

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion from the given prompt."""
        ...

    @abstractmethod
    def name(self) -> str:
        """Return the name of this provider."""
        ...


class LocalOllamaProvider(Provider):
    """Local provider for Ollama (llama.cpp / OpenWebUI compatible) - for GPU/local optimization.
    Self-hosted on RTX 5080 etc. Use for leaves / cost-efficient work in the pipeline.
    Supports system prompts, options (temp, max tokens), json format for structured responses.
    Integrates with tero/context/memory-gate via pre-built prompts in agent.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def name(self) -> str:
        return f"local-ollama ({self.model})"

    def complete(self, prompt: str, **kwargs: Any) -> str:
        import json
        import urllib.request

        # Allow overrides per-call (e.g. from agent for structured or task-specific)
        model = kwargs.get("model", self.model)
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        system = kwargs.get("system")
        use_json = kwargs.get("format_json", False)  # for StructuredResponse

        options = {
            "temperature": temperature,
            "num_predict": max_tokens,
        }

        # Prefer /api/chat for system + better multi-turn / tool future
        url = f"{self.base_url}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options,
        }
        if use_json:
            payload["format"] = "json"

        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:  # local can be slower
                res = json.loads(resp.read())
                # chat response shape
                if "message" in res and isinstance(res["message"], dict):
                    return res["message"].get("content", "")
                if "response" in res:  # fallback generate shape
                    return res.get("response", "")
                return str(res)
        except urllib.error.HTTPError as e:
            try:
                err = e.read().decode("utf-8", errors="replace")[:400]
            except Exception:
                err = str(e)
            raise RuntimeError(f"Local Ollama HTTP error: {e.code} {err}") from e
        except Exception as e:
            # Never silent - surface for agent event bus
            raise RuntimeError(f"[local-ollama error for {self.model}]: {e}") from e
