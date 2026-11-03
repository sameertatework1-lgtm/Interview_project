"""Contact form page object (on the home page)."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class ContactForm(BasePage):
    """The contact form section at the bottom of the home page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.name_input = page.get_by_placeholder("Name").or_(
            page.locator("#name, [data-testid='ContactName']")
        )
        self.email_input = page.get_by_placeholder("Email").or_(
            page.locator("#email, [data-testid='ContactEmail']")
        )
        self.phone_input = page.get_by_placeholder("Phone").or_(
            page.locator("#phone, [data-testid='ContactPhone']")
        )
        self.subject_input = page.get_by_placeholder("Subject").or_(
            page.locator("#subject, [data-testid='ContactSubject']")
        )
        self.message_input = page.locator(
            "textarea, input[placeholder*='Message'], [data-testid='ContactDescription']"
        ).first
        self.submit_button = page.get_by_role("button", name="Submit")
        self.success_banner = page.locator("h3:has-text('Thanks for getting in touch'), .alert-success").first
        self.error_messages = page.locator(".alert-danger, p.alert, .alert")

    def fill_and_submit(
        self,
        name: str,
        email: str,
        phone: str,
        subject: str,
        message: str,
    ) -> None:
        """Fill all fields and click Submit."""
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)
        self.subject_input.fill(subject)
        self.message_input.fill(message)
        self.submit_button.click()

    def submit_empty(self) -> None:
        """Click Submit without filling any fields."""
        self.submit_button.click()

    def expect_success(self, name: str) -> None:
        """Assert the success confirmation banner is visible."""
        self.expect_visible(self.success_banner)

    def expect_errors_visible(self) -> None:
        """Assert at least one validation error is visible."""
        self.expect_visible(self.error_messages.first)
