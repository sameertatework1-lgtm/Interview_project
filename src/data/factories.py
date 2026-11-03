"""Unique test-data factories — every entity uses AUTO_ prefix + timestamp + random."""

from __future__ import annotations

import random
import string
import time

from faker import Faker

_fake = Faker()


def _suffix() -> str:
    """Short unique suffix: epoch seconds + 4 random chars."""
    ts = str(int(time.time()))[-6:]
    rand = "".join(random.choices(string.ascii_lowercase, k=4))
    return f"{ts}{rand}"


# ── Room ──────────────────────────────────────────────────────────────────────


def room_payload(
    *,
    room_number: str | None = None,
    room_type: str = "Double",
    accessible: bool = False,
    price: int = 150,
    features: list[str] | None = None,
    description: str | None = None,
) -> dict:
    """Return a valid room creation payload with unique room number."""
    suffix = _suffix()
    return {
        "roomName": room_number or f"AUTO_{suffix}",
        "type": room_type,
        "accessible": accessible,
        "image": "https://www.mwtestconsultancy.co.uk/img/room2.jpg",
        "description": description or f"Auto-generated room {suffix}",
        "features": features or ["WiFi", "TV"],
        "roomPrice": price,
    }


# ── Booking ───────────────────────────────────────────────────────────────────


def booking_payload(
    room_id: int,
    *,
    checkin: str | None = None,
    checkout: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    deposit_paid: bool = False,
    email: str | None = None,
    phone: str | None = None,
) -> dict:
    """Return a valid booking creation payload."""
    suffix = _suffix()
    # Default: tomorrow to day after tomorrow
    import datetime

    today = datetime.date.today()
    ci = checkin or (today + datetime.timedelta(days=1)).isoformat()
    co = checkout or (today + datetime.timedelta(days=3)).isoformat()
    return {
        "roomid": room_id,
        "firstname": first_name or f"AUTO{suffix[:6]}",
        "lastname": last_name or f"Guest{suffix[6:]}",
        "depositpaid": deposit_paid,
        "bookingdates": {"checkin": ci, "checkout": co},
        "email": email or f"auto_{suffix}@test.example",
        "phone": phone or f"07700{suffix[:6]}",  # 11 digits
    }


# ── Message ───────────────────────────────────────────────────────────────────


def message_payload(
    *,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    subject: str | None = None,
    description: str | None = None,
) -> dict:
    """Return a valid contact message payload."""
    suffix = _suffix()
    return {
        "name": name or f"AUTO_{suffix}",
        "email": email or f"auto_{suffix}@test.example",
        "phone": phone or f"07700{suffix[:6]}",
        "subject": subject or f"AUTO Subject {suffix}",
        "description": description
        or f"Automated test message created at {suffix}. This is long enough.",
    }


# ── Branding ──────────────────────────────────────────────────────────────────


def branding_name() -> str:
    """Return a unique branding name for tests that update branding."""
    return f"AUTO_Brand_{_suffix()}"
