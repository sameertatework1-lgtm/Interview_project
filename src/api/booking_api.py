"""Booking API client."""

from __future__ import annotations

from playwright.sync_api import APIRequestContext, APIResponse

from config import settings
from src.api.base_client import BaseClient


class BookingAPI(BaseClient):
    """Wraps /api/booking endpoints."""

    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__(request_context, settings.API_BASE_URL + settings.BOOKING_PATH)

    def create_booking(self, payload: dict) -> APIResponse:
        """POST /api/booking — public endpoint, no token needed."""
        return self.post("", data=payload)

    def get_booking(self, booking_id: int, token: str) -> APIResponse:
        """GET /api/booking/{id} — admin token required."""
        return self.get(f"/{booking_id}", token=token)

    def list_bookings_by_room(self, room_id: int, token: str) -> APIResponse:
        """GET /api/booking?roomid={room_id} — admin token required."""
        return self.get(f"?roomid={room_id}", token=token)

    def get_summary(self, room_id: int) -> APIResponse:
        """GET /api/booking/summary?roomid={room_id} — public."""
        return self.get(f"/summary?roomid={room_id}")

    def update_booking(self, booking_id: int, payload: dict, token: str) -> APIResponse:
        """PUT /api/booking/{id} — admin token required."""
        return self.put(f"/{booking_id}", data=payload, token=token)

    def delete_booking(self, booking_id: int, token: str) -> APIResponse:
        """DELETE /api/booking/{id} — admin token required."""
        return self.delete(f"/{booking_id}", token=token)
