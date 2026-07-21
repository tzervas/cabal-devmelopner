"""Outbound status notify (E7.1) via tg-agent-relay.

Architecture (fleet-native):
  **Outbound** — this module shells out to ``relay-notify.sh`` (fire-and-forget).
  **Inbound** — platform-owned: ``tg-poll`` + FIFO keepalives write into backend
  FIFOs; the agent host (Grok/Claude) consumes those without cabal running a
  long-lived monitor. Cabal does **not** poll Telegram.

Never raises into the agent loop: notify failures are soft (return False + optional EventBus ERROR).
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from cabal_devmelopner.core.events import EventBus
from cabal_devmelopner.core.types import EventType


def resolve_relay_script(explicit: str | None = None) -> Path | None:
    """Locate relay-notify.sh from config, env, or well-known install paths."""
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    env = os.getenv("CABAL_RELAY_NOTIFY") or os.getenv("RELAY_NOTIFY")
    if env:
        candidates.append(env)
    home = Path.home()
    candidates.extend(
        [
            str(home / ".claude" / "telegram-bridge" / "relay-notify.sh"),
            str(home / ".grok" / "telegram-bridge" / "relay-notify.sh"),
            # sibling checkout relative to common work roots
            "/root/work/tg-agent-relay/relay-notify.sh",
            str(Path.cwd().parent / "tg-agent-relay" / "relay-notify.sh"),
        ]
    )
    for c in candidates:
        p = Path(c).expanduser()
        if p.is_file() and os.access(p, os.X_OK):
            return p.resolve()
        if p.is_file():
            # executable bit optional if we invoke via bash
            return p.resolve()
    return None


class Notifier(Protocol):
    def notify(self, text: str, *, label: str | None = None) -> bool: ...


@dataclass
class RelayNotifier:
    """Call tg-agent-relay ``relay-notify.sh`` for outbound Telegram status."""

    script: Path | None = None
    event_bus: EventBus | None = None
    enabled: bool = True
    timeout_sec: float = 30.0
    prefix: str = "cabal"

    def __post_init__(self) -> None:
        if self.script is None:
            self.script = resolve_relay_script()

    def notify(self, text: str, *, label: str | None = None) -> bool:
        if not self.enabled:
            return False
        if not text or not str(text).strip():
            return False
        script = self.script or resolve_relay_script()
        if script is None:
            self._emit_error(
                "notify: relay-notify.sh not found "
                "(set CABAL_RELAY_NOTIFY or install tg-agent-relay / telegram-bridge)"
            )
            return False
        body = str(text).strip()
        if len(body) > 3500:
            body = body[:3490] + "…"
        lab = label or self.prefix
        argv = ["bash", str(script), "--label", lab, body]
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                check=False,
                env={**os.environ, "TG_SEND_SOURCE": "hook"},
            )
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or f"exit {proc.returncode}")[:400]
                self._emit_error(f"notify: relay failed: {err}")
                return False
            return True
        except subprocess.TimeoutExpired:
            self._emit_error("notify: relay timed out")
            return False
        except Exception as e:
            self._emit_error(f"notify: {e}")
            return False

    def _emit_error(self, msg: str) -> None:
        if self.event_bus is not None:
            self.event_bus.emit_simple(EventType.ERROR, error=msg, source="notify")


class NullNotifier:
    """No-op notifier (default when notify disabled)."""

    def notify(self, text: str, *, label: str | None = None) -> bool:
        return False


def build_notifier(
    *,
    enabled: bool,
    script: str | None = None,
    event_bus: EventBus | None = None,
    on_complete: bool = True,
    on_error: bool = True,
) -> tuple[Notifier, dict[str, Any]]:
    """Factory returning notifier + flags for complete/error hooks."""
    flags = {"on_complete": on_complete and enabled, "on_error": on_error and enabled}
    if not enabled:
        return NullNotifier(), flags
    return (
        RelayNotifier(
            script=Path(script).expanduser() if script else None,
            event_bus=event_bus,
            enabled=True,
        ),
        flags,
    )
