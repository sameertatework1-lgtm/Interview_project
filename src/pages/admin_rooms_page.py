"""Admin rooms page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdminRoomsPage(BasePage):
    """Admin rooms management panel at /admin/rooms."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Room creation form
        self.room_name_input = page.locator("#roomName")
        self.room_type_select = page.locator("#type")
        self.accessible_select = page.locator("#accessible")
        self.room_price_input = page.locator("#roomPrice")
        self.create_button = page.locator("#createRoom, button:has-text('Create')")
        # Features checkboxes
        self.wifi_checkbox = page.locator("#wifiCheckbox")
        self.tv_checkbox = page.locator("#tvCheckbox")
        # Room rows
        self.room_rows = page.locator(
            ".room-listing, #rooms .row.hotel-room-info, div[data-testid='roomlisting']"
        )
        # Error
        self.error_banner = page.locator(".alert-danger")

    def navigate(self) -> None:
        """Open admin rooms page."""
        self.goto("/admin/rooms")

    def create_room(
        self,
        room_name: str,
        room_type: str = "Double",
        accessible: bool = False,
        price: int = 150,
        features: list[str] | None = None,
    ) -> None:
        """Fill and submit the room creation form."""
        self.room_name_input.fill(room_name)
        if self.room_type_select.count() > 0:
            self.room_type_select.select_option(room_type)
        if self.accessible_select.count() > 0:
            self.accessible_select.select_option("true" if accessible else "false")
        self.room_price_input.fill(str(price))
        if features:
            for feat in features:
                cb = self.page.locator(f"#{feat.lower()}Checkbox, label:has-text('{feat}') input")
                if cb.count() > 0 and not cb.first.is_checked():
                    cb.first.check()
        self.create_button.click()

    def room_exists_in_list(self, room_name: str) -> bool:
        """Return True if a room with the given name appears in the admin list."""
        return self.page.locator(f"text={room_name}").count() > 0

    def delete_room_by_name(self, room_name: str) -> None:
        """Click the delete button for a room with the given name."""
        row = self.page.locator("div, .row").filter(has_text=room_name)
        row.locator("span[id^='delete'], .fa-trash, .fa-remove").first.click()

    def expect_room_in_list(self, room_name: str) -> None:
        """Assert a room name is visible in the admin list."""
        self.expect_visible(self.page.locator(f"text={room_name}").first)
