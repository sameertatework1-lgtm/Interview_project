"""Branding API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class BrandingAPI(BaseClient):
    """Wraps /api/branding endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.BRANDING_PATH)

    def get_branding(self) -> APIResponse:
        """GET /api/branding — public."""
        return self.get("")

    def update_branding(self, payload: dict, token: str) -> APIResponse:
        """PUT /api/branding — admin token required."""
        return self.put("", data=payload, token=token)
