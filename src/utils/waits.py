"""Custom wait helpers — no time.sleep(), no wait_for_timeout()."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


def wait_for_url_contains(page: Page, fragment: str, timeout: int = 10_000) -> None:
    """Wait until the current URL contains *fragment*."""
    page.wait_for_url(f"**{fragment}**", timeout=timeout)


def wait_for_network_idle(page: Page, timeout: int = 10_000) -> None:
    """Wait for network to be idle (no more than 0 connections for 500 ms)."""
    page.wait_for_load_state("networkidle", timeout=timeout)


def expect_visible(locator: Locator, timeout: int = 10_000) -> None:
    """Assert a locator is visible within *timeout* ms."""
    expect(locator).to_be_visible(timeout=timeout)


def expect_hidden(locator: Locator, timeout: int = 10_000) -> None:
    """Assert a locator is hidden within *timeout* ms."""
    expect(locator).to_be_hidden(timeout=timeout)


def expect_text(locator: Locator, text: str, timeout: int = 10_000) -> None:
    """Assert locator contains *text* (case-insensitive substring)."""
    expect(locator).to_contain_text(text, timeout=timeout)
