"""xAI (Grok) provider using the raw Responses API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from cabal_devmelopner.providers.base import Provider


class XaiProvider(Provider):
    """Provider for xAI's Grok models via the raw API."""

    def __init__(self, api_key: str | None = None, model: str = "grok-4.5") -> None:
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY must be provided or set in environment")
        self.model = model
        self.base_url = "https://api.x.ai/v1/responses"

    def name(self) -> str:
        return f"xAI ({self.model})"

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Call the xAI Responses API."""
        payload = {
            "model": self.model,
            "input": prompt,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.base_url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
                # Handle common response shapes
                if isinstance(result, dict):
                    if result.get("output"):
                        return str(result["output"])
                    if result.get("choices"):
                        choice = result["choices"][0]
                        if isinstance(choice, dict):
                            content = choice.get("message", {}).get("content")
                            if content:
                                return str(content)
                    if result.get("content"):
                        return str(result["content"])
                return str(result)
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                error_body = "<unreadable>"
            raise RuntimeError(f"xAI API error ({e.code}): {error_body[:600]}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error calling xAI: {getattr(e, 'reason', e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error calling xAI API: {e}") from e
