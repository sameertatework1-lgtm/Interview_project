"""Playwright-based discovery script for Restful Booker Platform.

Captures real network calls, verifies endpoints, checks responses and status codes.
"""

import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "https://automationintesting.online")
API_BASE = os.environ.get("API_BASE_URL", "https://automationintesting.online/api")

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "docs" / "discovery_samples"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

findings = []


def run_discovery():
    print(f"--- Starting Playwright Discovery on {BASE_URL} ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        api = context.request

        # 1. First probe UI home page
        page = context.new_page()
        network_calls = []

        def on_response(response):
            if "/api/" in response.url or "/auth" in response.url or "/room" in response.url:
                try:
                    body = response.json()
                except Exception:
                    try:
                        body = response.text()
                    except Exception:
                        body = "<binary>"
                network_calls.append(
                    {
                        "url": response.url,
                        "method": response.request.method,
                        "status": response.status,
                        "body": body,
                    }
                )

        page.on("response", on_response)
        print("Navigating to home page...")
        page.goto(BASE_URL, wait_until="networkidle")
        print(f"Captured {len(network_calls)} API calls on home page load.")

        for call in network_calls:
            print(f"Captured UI call: {call['method']} {call['url']} -> {call['status']}")

        # 2. Test APIRequestContext directly
        def api_call(method, url, data=None, headers=None, save_name=None):
            full_url = url if url.startswith("http") else f"{API_BASE}{url}"
            req_headers = {"Content-Type": "application/json"}
            if headers:
                req_headers.update(headers)

            resp = api.fetch(
                full_url,
                method=method,
                data=json.dumps(data) if data is not None else None,
                headers=req_headers,
            )
            status = resp.status
            try:
                body = resp.json()
            except Exception:
                try:
                    body = resp.text()
                except Exception:
                    body = ""

            entry = {
                "method": method,
                "url": full_url,
                "status": status,
                "req_body": data,
                "resp_body": body,
            }
            if save_name:
                with open(SAMPLE_DIR / f"{save_name}.json", "w", encoding="utf-8") as f:
                    json.dump(entry, f, indent=2)
            findings.append(entry)
            print(f"[{method}] {full_url} -> {status}")
            return resp, body

        # Test 1: Auth actuator health
        _, h_body = api_call("GET", "/auth/actuator/health", save_name="auth_health")

        # Test 2: Room list
        _, r_body = api_call("GET", "/room/", save_name="room_list")

        # Test 3: Login valid
        login_res, login_body = api_call(
            "POST",
            "/auth/login",
            data={"username": "admin", "password": "password"},
            save_name="auth_login_valid",
        )
        token = None
        if isinstance(login_body, dict):
            token = login_body.get("token")

        # Check cookies in response
        for h in login_res.headers_array:
            if h["name"].lower() == "set-cookie" and "token=" in h["value"]:
                cookie_val = h["value"].split(";")[0].split("token=")[-1]
                if not token:
                    token = cookie_val
                print(f"Found cookie token: {cookie_val}")

        print(f"Token: {token}")
        auth_headers = {"Cookie": f"token={token}"} if token else {}

        # Test 4: Login invalid
        api_call(
            "POST",
            "/auth/login",
            data={"username": "admin", "password": "wrong"},
            save_name="auth_login_invalid",
        )

        # Test 5: Validate
        if token:
            api_call(
                "POST", "/auth/validate", data={"token": token}, save_name="auth_validate_valid"
            )
        api_call(
            "POST",
            "/auth/validate",
            data={"token": "invalid_123"},
            save_name="auth_validate_invalid",
        )

        # Test 6: Create room
        sample_room = {
            "roomName": f"AUTO_{int(time.time())}",
            "type": "Double",
            "accessible": True,
            "image": "https://www.mwtestconsultancy.co.uk/img/room2.jpg",
            "description": "Discovery test room",
            "features": ["WiFi", "TV"],
            "roomPrice": 120,
        }
        api_call("POST", "/room/", data=sample_room, save_name="room_create_no_token")
        create_room_res, create_room_body = api_call(
            "POST", "/room/", data=sample_room, headers=auth_headers, save_name="room_create_valid"
        )

        room_id = None
        if isinstance(create_room_body, dict):
            room_id = create_room_body.get("roomid")
        print(f"Room ID created: {room_id}")

        if room_id:
            api_call("GET", f"/room/{room_id}", save_name="room_get_by_id")
        api_call("GET", "/room/999999", save_name="room_get_nonexistent")

        # Test 7: Booking
        if room_id:
            booking_data = {
                "roomid": room_id,
                "firstname": "AutoFirst",
                "lastname": "AutoLast",
                "depositpaid": True,
                "bookingdates": {"checkin": "2099-01-10", "checkout": "2099-01-15"},
                "email": "auto@example.com",
                "phone": "012345678901",
            }
            create_b_res, create_b_body = api_call(
                "POST", "/booking/", data=booking_data, save_name="booking_create_valid"
            )
            bid = create_b_body.get("bookingid") if isinstance(create_b_body, dict) else None
            print(f"Booking ID created: {bid}")

            # Overlap
            api_call("POST", "/booking/", data=booking_data, save_name="booking_create_overlap")

            # Missing lastname
            bad_b = dict(booking_data)
            bad_b.pop("lastname")
            api_call("POST", "/booking/", data=bad_b, save_name="booking_create_missing_lastname")

            # Inverted dates
            inv_b = dict(booking_data)
            inv_b["bookingdates"] = {"checkin": "2099-01-20", "checkout": "2099-01-10"}
            api_call("POST", "/booking/", data=inv_b, save_name="booking_checkout_before_checkin")

            # Bookings by room
            api_call(
                "GET",
                f"/booking/?roomid={room_id}",
                headers=auth_headers,
                save_name="booking_list_by_room",
            )
            api_call("GET", f"/booking/summary?roomid={room_id}", save_name="booking_summary")

            if bid:
                api_call(
                    "GET",
                    f"/booking/{bid}",
                    headers=auth_headers,
                    save_name="booking_get_with_token",
                )
                api_call("GET", f"/booking/{bid}", save_name="booking_get_no_token")
                booking_data["firstname"] = "UpdatedName"
                api_call(
                    "PUT",
                    f"/booking/{bid}",
                    data=booking_data,
                    headers=auth_headers,
                    save_name="booking_update",
                )
                api_call(
                    "DELETE", f"/booking/{bid}", headers=auth_headers, save_name="booking_delete"
                )
                api_call(
                    "GET",
                    f"/booking/{bid}",
                    headers=auth_headers,
                    save_name="booking_get_after_delete",
                )

            # Delete room
            api_call("DELETE", f"/room/{room_id}", headers=auth_headers, save_name="room_delete")
            api_call("GET", f"/room/{room_id}", save_name="room_get_after_delete")

        # Test 8: Message
        msg_data = {
            "name": "Auto Contact",
            "email": "auto_contact@example.com",
            "phone": "012345678901",
            "subject": "Discovery Subject",
            "description": "This is a discovery test contact message longer than 20 chars.",
        }
        create_msg_res, create_msg_body = api_call(
            "POST", "/message/", data=msg_data, save_name="message_create_valid"
        )
        mid = create_msg_body.get("messageid") if isinstance(create_msg_body, dict) else None
        print(f"Message ID created: {mid}")

        bad_msg = dict(msg_data)
        bad_msg["description"] = "short"
        api_call("POST", "/message/", data=bad_msg, save_name="message_create_invalid")

        api_call("GET", "/message/", headers=auth_headers, save_name="message_list")
        if mid:
            api_call("GET", f"/message/{mid}", headers=auth_headers, save_name="message_get_by_id")
            api_call(
                "PUT", f"/message/{mid}/read", headers=auth_headers, save_name="message_mark_read"
            )
            api_call("DELETE", f"/message/{mid}", headers=auth_headers, save_name="message_delete")
            api_call(
                "GET", f"/message/{mid}", headers=auth_headers, save_name="message_get_after_delete"
            )

        # Test 9: Report & Branding
        api_call("GET", "/report/", headers=auth_headers, save_name="report_with_token")
        api_call("GET", "/report/", save_name="report_without_token")
        b_res, b_body = api_call("GET", "/branding/", save_name="branding_get")
        if isinstance(b_body, dict):
            new_b = dict(b_body)
            new_b["name"] = "AUTO_Temp"
            api_call(
                "PUT", "/branding/", data=new_b, headers=auth_headers, save_name="branding_update"
            )
            api_call(
                "PUT", "/branding/", data=b_body, headers=auth_headers, save_name="branding_restore"
            )

        # Test 10: Method not allowed
        api_call("PATCH", "/room/", data={}, save_name="general_patch_room")

        browser.close()
        print("\nPlaywright Discovery Finished Successfully!")


if __name__ == "__main__":
    run_discovery()
