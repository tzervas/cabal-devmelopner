"""Base classes for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


class Provider(ABC):
    """Abstract base class for model providers (xAI, Claude, local llama.cpp/Ollama, etc.).

    Supports self-hosted for cost/privacy/GPU optimization in workspace vision.
    """

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion from the given prompt."""
        ...

    def complete_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """Yield text chunks as they arrive (E4.1).

        Default: single chunk from ``complete``. Providers with native streaming
        should override for progressive CLI/TUI output.
        """
        yield self.complete(prompt, **kwargs)

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

    def _chat_payload(
        self, prompt: str, *, stream: bool, **kwargs: Any
    ) -> tuple[str, dict[str, Any]]:
        model = kwargs.get("model", self.model)
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        system = kwargs.get("system")
        use_json = kwargs.get("format_json", False)

        options = {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
        url = f"{self.base_url}/api/chat"
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": str(system)})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": options,
        }
        if use_json:
            payload["format"] = "json"
        return url, payload

    def complete(self, prompt: str, **kwargs: Any) -> str:
        import json
        import urllib.error
        import urllib.request

        url, payload = self._chat_payload(prompt, stream=False, **kwargs)
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:  # local can be slower
                res = json.loads(resp.read())
                if "message" in res and isinstance(res["message"], dict):
                    return res["message"].get("content", "")
                if "response" in res:
                    return res.get("response", "")
                return str(res)
        except urllib.error.HTTPError as e:
            try:
                err = e.read().decode("utf-8", errors="replace")[:400]
            except Exception:
                err = str(e)
            raise RuntimeError(f"Local Ollama HTTP error: {e.code} {err}") from e
        except Exception as e:
            raise RuntimeError(f"[local-ollama error for {self.model}]: {e}") from e

    def complete_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """Stream Ollama chat NDJSON chunks (E4.1)."""
        import json
        import urllib.error
        import urllib.request

        url, payload = self._chat_payload(prompt, stream=True, **kwargs)
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                for raw in resp:
                    line = raw.decode("utf-8", errors="replace").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = obj.get("message") or {}
                    piece = msg.get("content") if isinstance(msg, dict) else None
                    if piece:
                        yield str(piece)
                    elif obj.get("response"):
                        yield str(obj["response"])
                    if obj.get("done"):
                        break
        except urllib.error.HTTPError as e:
            try:
                err = e.read().decode("utf-8", errors="replace")[:400]
            except Exception:
                err = str(e)
            raise RuntimeError(f"Local Ollama HTTP error: {e.code} {err}") from e
        except Exception as e:
            raise RuntimeError(f"[local-ollama stream error for {self.model}]: {e}") from e
