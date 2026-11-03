"""BasePage: shared locator helpers and navigation used by all page objects."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """All page objects inherit from this class.

    Rules (per SKILL.md):
    - Locators are defined here or in subclasses, never in step defs.
    - No assertions inside page objects except small expect_* helpers.
    - Locator priority: role > label > placeholder > text > id/data-testid > CSS.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.timeout = settings.DEFAULT_TIMEOUT_MS

    # ── Navigation ────────────────────────────────────────────────────────────

    def goto(self, path: str = "") -> None:
        """Navigate to BASE_URL + path with fallback for shared demo lag."""
        url = settings.BASE_URL.rstrip("/") + path
        logger.debug("Navigating to %s", url)
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=15_000)
        except Exception:
            self.page.goto(url, wait_until="commit", timeout=15_000)

    def reload(self) -> None:
        self.page.reload(wait_until="domcontentloaded")

    # ── Assertions (small helpers only) ───────────────────────────────────────

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**", timeout=self.timeout)

    def expect_visible(self, locator, *, timeout: int | None = None) -> None:
        expect(locator).to_be_visible(timeout=timeout or self.timeout)

    def expect_text(self, locator, text: str, *, timeout: int | None = None) -> None:
        expect(locator).to_contain_text(text, timeout=timeout or self.timeout)

    # ── JavaScript helpers ────────────────────────────────────────────────────

    def has_horizontal_overflow(self) -> bool:
        """Return True if the page body scrolls horizontally (responsive check)."""
        return self.page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
