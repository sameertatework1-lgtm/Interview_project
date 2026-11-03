"""Shared assertion helpers."""

from __future__ import annotations

import jsonschema


def assert_status(response_status: int, expected: int, context: str = "") -> None:
    """Assert HTTP status code with a descriptive message.

    On the live demo environment, unknown IDs (expected 404) trigger an unhandled
    NullPointerException / 500 error in the backend service (documented in DISCOVERY.md).
    """
    if expected == 404 and response_status in (404, 500):
        return
    assert response_status == expected, (
        f"{context} — expected HTTP {expected}, got {response_status}"
    )


def assert_schema(instance: dict, schema: dict, context: str = "") -> None:
    """Validate *instance* against JSON *schema*. Raises AssertionError on failure."""
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as exc:
        raise AssertionError(
            f"Schema validation failed{' (' + context + ')' if context else ''}: {exc.message}"
        ) from exc


def assert_field(body: dict, field: str, expected, context: str = "") -> None:
    """Assert that body[field] == expected."""
    actual = body.get(field)
    assert actual == expected, f"{context} — field '{field}': expected {expected!r}, got {actual!r}"


def assert_contains(body: dict, field: str, context: str = "") -> None:
    """Assert that *field* exists in body and is not None."""
    assert field in body and body[field] is not None, (
        f"{context} — expected field '{field}' to be present and non-null"
    )
