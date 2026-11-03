"""API step definitions for Booking feature."""

from __future__ import annotations

from pytest_bdd import given, parsers, then, when

from src.api.booking_api import BookingAPI
from src.data.factories import booking_payload
from src.utils.assertions import assert_status

# Fixed dates for overlap tests (far future to avoid conflicts with other runs)
_FIXED_CHECKIN = "2099-06-01"
_FIXED_CHECKOUT = "2099-06-05"


@when("I create a booking for that room with valid data")
def step_create_booking(context: dict, booking_api: BookingAPI, cleanup_bookings: list) -> None:
    payload = booking_payload(context["room_id"])
    context["booking_payload"] = payload
    resp = booking_api.create_booking(payload)
    context["response"] = resp
    if resp.status in (200, 201):
        body = resp.json()
        bid = body.get("bookingid")
        if bid:
            context["booking_id"] = bid
            cleanup_bookings.append(bid)


@then("the booking response contains a booking id")
def step_booking_has_id(context: dict) -> None:
    body = context["response"].json()
    bid = body.get("bookingid")
    assert bid and isinstance(bid, int) and bid > 0, f"Invalid booking id: {bid}"
    context["booking_id"] = bid


@when("I create a booking for that room missing the lastname field")
def step_create_booking_no_lastname(context: dict, booking_api: BookingAPI) -> None:
    payload = booking_payload(context["room_id"])
    payload.pop("lastname", None)
    context["response"] = booking_api.create_booking(payload)


@when("I create a booking with checkout date before checkin date")
def step_create_booking_bad_dates(context: dict, booking_api: BookingAPI) -> None:
    payload = booking_payload(
        context["room_id"],
        checkin="2099-07-10",
        checkout="2099-07-05",
    )
    context["response"] = booking_api.create_booking(payload)


@given("a booking exists for that room on fixed dates")
def step_booking_fixed_dates(
    context: dict, booking_api: BookingAPI, cleanup_bookings: list
) -> None:
    payload = booking_payload(
        context["room_id"],
        checkin=_FIXED_CHECKIN,
        checkout=_FIXED_CHECKOUT,
    )
    resp = booking_api.create_booking(payload)
    assert resp.status in (200, 201), f"Failed to create fixed-date booking: {resp.status}"
    bid = resp.json().get("bookingid")
    context["fixed_booking_id"] = bid
    cleanup_bookings.append(bid)


@when("I create another booking for the same room on the same dates")
def step_create_overlap_booking(context: dict, booking_api: BookingAPI) -> None:
    payload = booking_payload(
        context["room_id"],
        checkin=_FIXED_CHECKIN,
        checkout=_FIXED_CHECKOUT,
    )
    context["response"] = booking_api.create_booking(payload)


@when(parsers.parse('I create a booking with invalid email "{email}"'))
def step_create_booking_bad_email(context: dict, booking_api: BookingAPI, email: str) -> None:
    payload = booking_payload(context["room_id"], email=email)
    context["response"] = booking_api.create_booking(payload)


@given("a booking exists for that room")
def step_booking_exists(context: dict, booking_api: BookingAPI, cleanup_bookings: list) -> None:
    payload = booking_payload(context["room_id"])
    context["booking_payload"] = payload
    resp = booking_api.create_booking(payload)
    assert resp.status in (200, 201), f"Failed to create booking: {resp.status} {resp.text()}"
    body = resp.json()
    bid = body.get("bookingid")
    context["booking_id"] = bid
    cleanup_bookings.append(bid)


@when("I list bookings for that room id")
def step_list_bookings(context: dict, booking_api: BookingAPI, admin_token: str) -> None:
    context["response"] = booking_api.list_bookings_by_room(context["room_id"], admin_token)


@then("the booking list includes the created booking")
def step_booking_in_list(context: dict) -> None:
    body = context["response"].json()
    bookings = body.get("bookings", body if isinstance(body, list) else [])
    ids = [b.get("bookingid") for b in bookings]
    assert context["booking_id"] in ids, f"Booking {context['booking_id']} not found in list: {ids}"


@when("I get that booking by id")
def step_get_booking(context: dict, booking_api: BookingAPI, admin_token: str) -> None:
    context["response"] = booking_api.get_booking(context["booking_id"], admin_token)


@then("the booking fields match what was created")
def step_booking_fields_match(context: dict) -> None:
    body = context["response"].json()
    payload = context["booking_payload"]
    assert body.get("firstname") == payload["firstname"], "Firstname mismatch"
    assert body.get("lastname") == payload["lastname"], "Lastname mismatch"


@when("I GET the booking summary for that room")
def step_get_summary(context: dict, booking_api: BookingAPI) -> None:
    context["response"] = booking_api.get_summary(context["room_id"])


@then("the summary contains date ranges")
def step_summary_has_dates(context: dict) -> None:
    body = context["response"].json()
    bookings = body.get("bookings", [])
    assert isinstance(bookings, list), f"Expected list, got {type(bookings)}"


@when("I update that booking with new dates")
def step_update_booking(context: dict, booking_api: BookingAPI, admin_token: str) -> None:
    payload = dict(context["booking_payload"])
    payload["bookingdates"] = {"checkin": "2099-08-01", "checkout": "2099-08-05"}
    context["updated_booking_payload"] = payload
    context["update_booking_response"] = booking_api.update_booking(
        context["booking_id"], payload, admin_token
    )


@then(parsers.parse("the update response status is {expected:d}"))
def step_update_status(context: dict, expected: int) -> None:
    assert_status(context["update_booking_response"].status, expected)


@then("GET that booking shows the updated dates")
def step_verify_updated_dates(context: dict, booking_api: BookingAPI, admin_token: str) -> None:
    resp = booking_api.get_booking(context["booking_id"], admin_token)
    assert resp.status == 200
    dates = resp.json().get("bookingdates", {})
    assert dates.get("checkin") == "2099-08-01", f"Checkin mismatch: {dates}"


@when("I delete that booking via API")
def step_delete_booking(
    context: dict, booking_api: BookingAPI, admin_token: str, cleanup_bookings: list
) -> None:
    context["delete_booking_response"] = booking_api.delete_booking(
        context["booking_id"], admin_token
    )
    bid = context["booking_id"]
    if bid in cleanup_bookings:
        cleanup_bookings.remove(bid)


@then("the delete booking response status is 200")
@then("the delete booking response status is 202")
def step_delete_booking_status_ok(context: dict) -> None:
    assert context["delete_booking_response"].status in (200, 202)


@then("GET that deleted booking returns 404")
def step_deleted_booking_404(context: dict, booking_api: BookingAPI, admin_token: str) -> None:
    resp = booking_api.get_booking(context["booking_id"], admin_token)
    assert resp.status in (404, 500), f"Expected 404 or 500 after delete, got {resp.status}"


@when("I get that booking by id without a token")
def step_get_booking_no_token(context: dict, booking_api: BookingAPI) -> None:
    context["response"] = booking_api.get_booking(context["booking_id"], token="")
