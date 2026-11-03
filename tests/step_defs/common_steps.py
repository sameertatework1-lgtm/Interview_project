"""Common steps shared across API, UI and E2E step definitions."""

from __future__ import annotations

from pytest_bdd import given, parsers, then

from src.utils.assertions import assert_status


@given("the API is available")
def api_is_available(health_check):  # noqa: ARG001
    """Health check fixture (session-autouse) ensures the API is up."""


@given("I have a valid admin token")
def step_have_admin_token(context: dict, admin_token: str) -> None:
    context["token"] = admin_token


@then(parsers.parse("the response status is {expected_status:d}"))
def step_assert_status(context: dict, expected_status: int) -> None:
    assert_status(context["response"].status, expected_status)


@then(parsers.parse("the response body contains {text}"))
def step_response_body_contains(context: dict, text: str) -> None:
    body = context["response"].text()
    assert text.strip('"') in body, f"Expected '{text}' in response body, got: {body[:200]}"
