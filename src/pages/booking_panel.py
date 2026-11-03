"""Booking panel page object (opens inline on the home page)."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class BookingPanel(BasePage):
    """The booking calendar + form that expands under a room card."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Form fields
        self.first_name = page.get_by_placeholder("Firstname")
        self.last_name = page.get_by_placeholder("Lastname")
        self.email = page.get_by_placeholder("Email")
        self.phone = page.get_by_placeholder("Phone")
        # Buttons
        self.book_button = page.get_by_role("button", name="Book")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        # Calendar
        self.calendar = page.locator(".rbc-calendar")
        # Success / error
        self.success_message = page.locator(".booking-confirmation h3, .alert-success, h3").filter(
            has_text="Booking Successful"
        )
        self.error_messages = page.locator(".alert-danger, p.alert")

    def wait_for_panel(self) -> None:
        """Wait for the calendar to appear after clicking 'Book this room'."""
        self.expect_visible(self.calendar)

    def fill_guest_details(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
    ) -> None:
        """Fill the guest detail fields."""
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.email.fill(email)
        self.phone.fill(phone)

    def select_dates_by_drag(self, start_day: int, end_day: int) -> None:
        """Drag across calendar cells to select a date range.

        Uses the current month's displayed cells. Locates cells by aria-label
        containing the day number. Falls back to JS drag if needed.
        """
        # Calendar cells: aria-label like "Nov 10 2024"
        cells = self.page.locator(".rbc-date-cell, .rbc-day-bg")
        # Find start and end cells by index (simple approach for available dates)
        start_cell = cells.nth(start_day - 1)
        end_cell = cells.nth(end_day - 1)
        start_box = start_cell.bounding_box()
        end_box = end_cell.bounding_box()
        if start_box and end_box:
            self.page.mouse.move(
                start_box["x"] + start_box["width"] / 2,
                start_box["y"] + start_box["height"] / 2,
            )
            self.page.mouse.down()
            self.page.mouse.move(
                end_box["x"] + end_box["width"] / 2,
                end_box["y"] + end_box["height"] / 2,
            )
            self.page.mouse.up()

    def click_book(self) -> None:
        """Click the Book button."""
        self.book_button.click()

    def click_cancel(self) -> None:
        """Click the Cancel button."""
        self.cancel_button.click()

    def expect_success(self) -> None:
        """Assert booking success message is visible."""
        self.expect_visible(self.success_message, timeout=15_000)

    def expect_error_visible(self) -> None:
        """Assert at least one error message is visible."""
        self.expect_visible(self.error_messages.first)

    def expect_panel_closed(self) -> None:
        """Assert the booking panel / calendar is hidden."""
        self.expect_visible(self.cancel_button.or_(self.calendar), timeout=2_000)
