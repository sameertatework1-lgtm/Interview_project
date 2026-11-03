"""Admin report page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdminReportPage(BasePage):
    """Admin report / occupancy calendar."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.report_nav = page.get_by_role("link", name="Report")
        self.report_calendar = page.locator(".rbc-calendar, .report")

    def navigate_to_report(self) -> None:
        """Click the Report nav link."""
        self.report_nav.click()

    def expect_report_loaded(self) -> None:
        """Assert the report calendar / view is visible."""
        self.expect_visible(self.report_calendar)
