"""API step definitions for Auth feature."""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, then, when

from src.api.auth_api import AuthAPI
from src.utils.assertions import assert_status


@when(parsers.parse('I login via API with username "{username}" and password "{password}"'))
def step_login_api(context: dict, auth_api: AuthAPI, username: str, password: str) -> None:
    context["response"] = auth_api.login(username, password)


@when(parsers.parse('I GET "{path}"'))
def step_get_path(context: dict, auth_api: AuthAPI, api_request_context, path: str) -> None:
    """Generic GET step using the raw API request context."""
    import time

    from config import settings

    url = settings.BASE_URL.rstrip("/") + path
    t0 = time.monotonic()
    resp = api_request_context.get(url)
    context["response"] = resp
    context["response_time_ms"] = (time.monotonic() - t0) * 1000
    if path == "/api/auth/actuator/health" and resp.status == 500:
        pytest.xfail("API-001: Actuator health endpoint returns HTTP 500 on live public demo.")


@when(parsers.parse('I POST "{path}" with body:'))
def step_post_with_body(context: dict, api_request_context, path: str, docstring: str) -> None:
    from config import settings

    url = settings.BASE_URL.rstrip("/") + path
    resp = api_request_context.post(
        url, data=docstring, headers={"Content-Type": "application/json"}
    )
    context["response"] = resp


@then("the response contains a token")
def step_response_has_token(context: dict) -> None:
    body = context["response"].json()
    assert "token" in body and body["token"], f"No token in response: {body}"
    context["token"] = body["token"]


@given("I have a valid admin token")
def step_given_admin_token(context: dict, admin_token: str) -> None:
    context["token"] = admin_token


@given("I obtain a fresh token for logout test")
def step_fresh_token(context: dict, auth_api: AuthAPI) -> None:
    from config import settings

    context["logout_token"] = auth_api.get_token(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)


@when("I validate the admin token")
def step_validate_admin_token(context: dict, auth_api: AuthAPI) -> None:
    context["response"] = auth_api.validate(context["token"])


@when("I logout with that token")
def step_logout(context: dict, auth_api: AuthAPI) -> None:
    context["logout_response"] = auth_api.logout(context["logout_token"])


@then(parsers.parse("the logout response status is {expected:d}"))
def step_logout_status(context: dict, expected: int) -> None:
    assert_status(context["logout_response"].status, expected)


@when("I validate that token after logout")
def step_validate_after_logout(context: dict, auth_api: AuthAPI) -> None:
    context["validate_after_logout"] = auth_api.validate(context["logout_token"])


@then(parsers.parse("the validate response status is {expected:d}"))
def step_validate_after_logout_status(context: dict, expected: int) -> None:
    assert_status(context["validate_after_logout"].status, expected)
