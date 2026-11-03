"""Report API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class ReportAPI(BaseClient):
    """Wraps /api/report endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.REPORT_PATH)

    def get_report(self, token: str) -> APIResponse:
        """GET /api/report — admin token required."""
        return self.get("", token=token)
