"""E2E test runner — loads all E2E feature files."""

from pytest_bdd import scenarios

scenarios("../features/e2e")
