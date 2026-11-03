"""Admin messages page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdminMessagesPage(BasePage):
    """Admin messages / inbox panel."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.messages_nav = page.get_by_role("link", name="Inbox")
        self.message_rows = page.locator(".message-body, .messages .row")
        self.message_details = page.locator(".message")

    def navigate_to_inbox(self) -> None:
        """Click the Inbox nav link."""
        self.messages_nav.click()

    def message_with_subject_visible(self, subject: str) -> bool:
        """Return True if a message with the given subject is in the list."""
        return self.page.locator(".message-body, .messages").filter(has_text=subject).count() > 0

    def click_message(self, subject: str) -> None:
        """Click a message row by subject text."""
        self.page.locator(".message-body").filter(has_text=subject).first.click()

    def delete_message_by_subject(self, subject: str) -> None:
        """Click the delete icon next to a message."""
        row = self.page.locator(".message-body").filter(has_text=subject).first
        row.locator("span[id^='delete']").click()
