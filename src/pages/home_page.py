"""Home page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class HomePage(BasePage):
    """Public home page at /."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locators
        self.room_cards = page.locator(
            ".hotel-room-info, div:has(a[href*='/reservation']), div.col-sm-7"
        )
        self.contact_form = page.locator("#contact, div:has-text('Send Us a Message')")
        self.footer = page.locator("footer, [role='contentinfo']")
        self.branding_logo = page.locator(".hotel-logoUrl, .navbar-brand, h1, .hotel-name")
        self.book_buttons = page.get_by_role("link", name="Book now").or_(
            page.get_by_role("button", name="Book this room")
        )
        self.hotel_name = page.locator(".hotel-name, h1")

    def navigate(self) -> None:
        """Open the home page."""
        self.goto("/")

    def get_room_card_count(self) -> int:
        """Return number of visible room cards."""
        self.book_buttons.first.wait_for(state="visible", timeout=self.timeout)
        return self.book_buttons.count()

    def get_room_names(self) -> list[str]:
        """Return text of all room name headings."""
        cards = self.room_cards.all()
        names = []
        for card in cards:
            name_el = card.locator("h3, h5, .room-name")
            if name_el.count() > 0:
                names.append(name_el.first.inner_text().strip())
        return names

    def click_book_first_room(self) -> None:
        """Click 'Book now' on the first room."""
        self.book_buttons.first.click()

    def click_book_room_by_name(self, room_name: str) -> None:
        """Find a room card by name and click its Book button."""
        card = self.page.locator("div").filter(has_text=room_name)
        card.get_by_role("link", name="Book now").or_(
            card.get_by_role("button", name="Book this room")
        ).first.click()

    def room_card_with_name_visible(self, room_name: str) -> bool:
        """Return True if a room card containing room_name is visible."""
        card = self.page.locator("div").filter(has_text=room_name)
        return card.count() > 0

    def get_first_room_price(self) -> str:
        """Return the price text shown on the first room card."""
        return self.page.locator("text=per night").first.inner_text()
