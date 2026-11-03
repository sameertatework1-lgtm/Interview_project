"""Admin login page object."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdminLoginPage(BasePage):
    """Admin login form at /admin."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator("#username, input[placeholder*='sername']")
        self.password_input = page.locator("#password, input[placeholder*='assword']")
        self.login_button = page.locator("#doLogin, button:has-text('Login')")
        self.error_message = page.locator(
            ".alert-danger, .invalid-credentials, p:has-text('Invalid')"
        )
        # After login
        self.rooms_panel = page.locator("#roomName").or_(page.get_by_text("Room #")).first
        self.logout_button = page.get_by_role("button", name="Logout")
        self.admin_nav = page.locator(".navbar-nav, .admin-nav")

    def navigate(self) -> None:
        """Open admin login page."""
        self.goto("/admin")

    def login(self, username: str, password: str) -> None:
        """Fill credentials and click Login."""
        self.username_input.wait_for(state="visible", timeout=self.timeout)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self) -> None:
        """Click the Logout button."""
        self.logout_button.click()

    def expect_logged_in(self) -> None:
        """Assert admin dashboard is visible."""
        self.expect_visible(self.rooms_panel)

    def expect_login_error(self) -> None:
        """Assert an error message is shown on bad credentials."""
        self.expect_visible(self.error_message)

    def expect_on_login_page(self) -> None:
        """Assert the login form is still visible (not redirected)."""
        self.expect_visible(self.login_button)
