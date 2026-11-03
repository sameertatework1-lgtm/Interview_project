"""Room API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class RoomAPI(BaseClient):
    """Wraps /api/room endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.ROOM_PATH)

    def list_rooms(self) -> APIResponse:
        """GET /api/room"""
        return self.get("")

    def get_room(self, room_id: int) -> APIResponse:
        """GET /api/room/{id}"""
        return self.get(f"/{room_id}")

    def create_room(self, payload: dict, token: str) -> APIResponse:
        """POST /api/room"""
        return self.post("", data=payload, token=token)

    def update_room(self, room_id: int, payload: dict, token: str) -> APIResponse:
        """PUT /api/room/{id}"""
        return self.put(f"/{room_id}", data=payload, token=token)

    def delete_room(self, room_id: int, token: str) -> APIResponse:
        """DELETE /api/room/{id}"""
        return self.delete(f"/{room_id}", token=token)
