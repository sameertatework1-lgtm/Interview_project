"""Message API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class MessageAPI(BaseClient):
    """Wraps /api/message endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.MESSAGE_PATH)

    def create_message(self, payload: dict) -> APIResponse:
        """POST /api/message — public."""
        return self.post("", data=payload)

    def list_messages(self, token: str) -> APIResponse:
        """GET /api/message — admin token required."""
        return self.get("", token=token)

    def get_message(self, message_id: int, token: str) -> APIResponse:
        """GET /api/message/{id} — admin token required."""
        return self.get(f"/{message_id}", token=token)

    def mark_read(self, message_id: int, token: str) -> APIResponse:
        """PUT /api/message/{id}/read — admin token required."""
        return self.put(f"/{message_id}/read", token=token)

    def delete_message(self, message_id: int, token: str) -> APIResponse:
        """DELETE /api/message/{id} — admin token required."""
        return self.delete(f"/{message_id}", token=token)
