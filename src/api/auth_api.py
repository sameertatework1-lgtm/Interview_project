"""Auth API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class AuthAPI(BaseClient):
    """Wraps /api/auth endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.AUTH_PATH)

    def health(self) -> APIResponse:
        """GET /api/auth/actuator/health"""
        return self.get("/actuator/health")

    def login(self, username: str, password: str) -> APIResponse:
        """POST /api/auth/login"""
        return self.post("/login", data={"username": username, "password": password})

    def logout(self, token: str) -> APIResponse:
        """POST /api/auth/logout"""
        return self.post("/logout", token=token)

    def validate(self, token: str) -> APIResponse:
        """POST /api/auth/validate"""
        return self.post("/validate", data={"token": token})

    def get_token(self, username: str | None = None, password: str | None = None) -> str:
        """Login and return the token string. Raises on failure."""
        resp = self.login(
            username or settings.ADMIN_USERNAME,
            password or settings.ADMIN_PASSWORD,
        )
        assert resp.status == 200, f"Login failed: {resp.status} {resp.text()}"
        body = resp.json()
        token = body.get("token")
        assert token, f"No token in login response: {body}"
        return token
