"""pytest conftest.py: fixtures, hooks, health check, cleanup."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import (
    APIRequestContext,
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from config import settings
from src.api.auth_api import AuthAPI
from src.api.booking_api import BookingAPI
from src.api.branding_api import BrandingAPI
from src.api.message_api import MessageAPI
from src.api.room_api import RoomAPI
from src.utils.logger import get_logger
from tests.step_defs.api_steps.auth_steps import *
from tests.step_defs.api_steps.booking_steps import *
from tests.step_defs.api_steps.misc_steps import *
from tests.step_defs.api_steps.room_steps import *

# Import all step definitions so pytest-bdd scenarios can resolve them everywhere
from tests.step_defs.common_steps import *
from tests.step_defs.e2e_steps.e2e_steps import *
from tests.step_defs.ui_steps.ui_steps import *

logger = get_logger("conftest")

# ── Directories ───────────────────────────────────────────────────────────────

SCREENSHOTS_DIR = Path("reports/screenshots")
TRACES_DIR = Path("reports/traces")
VIDEOS_DIR = Path("reports/videos")
for _d in (SCREENSHOTS_DIR, TRACES_DIR, VIDEOS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ── Session-level Playwright / API context ────────────────────────────────────


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def api_request_context(
    playwright_instance: Playwright,
) -> Generator[APIRequestContext, None, None]:
    ctx = playwright_instance.request.new_context(
        base_url=settings.BASE_URL,
        extra_http_headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        },
    )
    yield ctx
    ctx.dispose()


# ── Session health check ───────────────────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def health_check(api_request_context: APIRequestContext) -> None:
    """Verify target system is reachable before running any tests."""
    try:
        resp = api_request_context.get(f"{settings.BASE_URL}/api/room")
        if resp.status not in (200, 201):
            pytest.skip(f"Health check failed: HTTP {resp.status}. Site may be down or resetting.")
        logger.info("Health check passed: /api/room returned HTTP %d", resp.status)
    except Exception as exc:
        pytest.skip(f"Site unreachable: {exc}")


# ── Session token ─────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def admin_token(api_request_context: APIRequestContext) -> str:
    """Obtain and cache the admin token for the whole session."""
    auth_api = AuthAPI(api_request_context)
    token = auth_api.get_token()
    logger.info("Admin token obtained (cached for session).")
    return token


# ── Per-test context dict (step-to-step shared state) ─────────────────────────


@pytest.fixture()
def context() -> dict:
    """Mutable dict for sharing state between steps. Never use globals."""
    return {}


# ── API client fixtures ───────────────────────────────────────────────────────


@pytest.fixture()
def auth_api(api_request_context: APIRequestContext) -> AuthAPI:
    return AuthAPI(api_request_context)


@pytest.fixture()
def room_api(api_request_context: APIRequestContext) -> RoomAPI:
    return RoomAPI(api_request_context)


@pytest.fixture()
def booking_api(api_request_context: APIRequestContext) -> BookingAPI:
    return BookingAPI(api_request_context)


@pytest.fixture()
def message_api(api_request_context: APIRequestContext) -> MessageAPI:
    return MessageAPI(api_request_context)


@pytest.fixture()
def branding_api(api_request_context: APIRequestContext) -> BrandingAPI:
    return BrandingAPI(api_request_context)


# ── Data-cleanup fixtures ─────────────────────────────────────────────────────


@pytest.fixture()
def cleanup_rooms(room_api: RoomAPI, admin_token: str):
    """Yield a list; any room ids appended are deleted in teardown."""
    ids: list = []
    yield ids
    for rid in ids:
        if rid:
            try:
                room_api.delete_room(rid, admin_token)
                logger.info("Cleaned up room %s", rid)
            except Exception as exc:
                logger.warning("Cleanup room %s failed: %s", rid, exc)


@pytest.fixture()
def cleanup_bookings(booking_api: BookingAPI, admin_token: str):
    """Yield a list; any booking ids appended are deleted in teardown."""
    ids: list = []
    yield ids
    for bid in ids:
        if bid:
            try:
                booking_api.delete_booking(bid, admin_token)
                logger.info("Cleaned up booking %s", bid)
            except Exception as exc:
                logger.warning("Cleanup booking %s failed: %s", bid, exc)


@pytest.fixture()
def cleanup_messages(message_api: MessageAPI, admin_token: str):
    """Yield a list; any message ids appended are deleted in teardown."""
    ids: list = []
    yield ids
    for mid in ids:
        if mid:
            try:
                message_api.delete_message(mid, admin_token)
                logger.info("Cleaned up message %s", mid)
            except Exception as exc:
                logger.warning("Cleanup message %s failed: %s", mid, exc)


# ── Browser fixtures ──────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    browser = playwright_instance.chromium.launch(
        headless=settings.HEADLESS,
        slow_mo=settings.BROWSER_SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture()
def browser_context(browser: Browser, tmp_path) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        record_video_dir=str(VIDEOS_DIR) if os.environ.get("RECORD_VIDEO") else None,
    )
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.close()


@pytest.fixture()
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    page = browser_context.new_page()
    page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    yield page


# ── Failure hooks ─────────────────────────────────────────────────────────────


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture:
            screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
            try:
                page_fixture.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
            ctx = page_fixture.context
            trace_path = TRACES_DIR / f"{item.name}.zip"
            try:
                ctx.tracing.stop(path=str(trace_path))
                allure.attach.file(
                    str(trace_path),
                    name="trace",
                    attachment_type=allure.attachment_type.ZIP,
                )
            except Exception:
                pass
