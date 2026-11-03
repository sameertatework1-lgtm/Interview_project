"""env-driven configuration — all values come from .env; no hard-coding."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env if present (CI injects env vars directly)
load_dotenv(Path(__file__).parent.parent / ".env")


def _require(key: str) -> str:
    """Return env var or raise a clear error."""
    value = os.environ.get(key)
    if not value:
        raise OSError(
            f"Required env var '{key}' is not set. Copy .env.example to .env and fill it in."
        )
    return value


# ── Target system ─────────────────────────────────────────────────────────────
BASE_URL: str = os.environ.get("BASE_URL", "https://automationintesting.online")
API_BASE_URL: str = os.environ.get("API_BASE_URL", "https://automationintesting.online/api")

ADMIN_USERNAME: str = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "password")

# ── Browser ───────────────────────────────────────────────────────────────────
HEADLESS: bool = os.environ.get("HEADLESS", "true").lower() == "true"
BROWSER_SLOW_MO: int = int(os.environ.get("BROWSER_SLOW_MO", "0"))
DEFAULT_TIMEOUT_MS: int = int(os.environ.get("DEFAULT_TIMEOUT_MS", "30000"))

# ── Parallelism ───────────────────────────────────────────────────────────────
WORKERS: int = min(int(os.environ.get("WORKERS", "1")), 2)  # max 2 per SKILL.md

# ── API paths (confirmed by DISCOVERY.md) ────────────────────────────────────
AUTH_PATH = "/auth"
ROOM_PATH = "/room"
BOOKING_PATH = "/booking"
MESSAGE_PATH = "/message"
REPORT_PATH = "/report"
BRANDING_PATH = "/branding"
