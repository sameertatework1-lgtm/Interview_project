"""Admin branding page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdminBrandingPage(BasePage):
    """Admin branding configuration panel."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.branding_nav = page.get_by_role("link", name="Branding")
        self.hotel_name_input = page.locator("#hotelName, input[name='hotelName']").or_(
            page.get_by_label("Hotel Name")
        )
        self.save_button = page.get_by_role("button", name="Submit").or_(
            page.get_by_role("button", name="Save")
        )

    def navigate_to_branding(self) -> None:
        """Click the Branding nav link."""
        self.branding_nav.click()

    def update_hotel_name(self, new_name: str) -> None:
        """Clear and retype the hotel name, then save."""
        self.hotel_name_input.clear()
        self.hotel_name_input.fill(new_name)
        self.save_button.click()

    def get_hotel_name(self) -> str:
        """Return the current hotel name value."""
        return self.hotel_name_input.input_value()
