"""API test runner — loads all API feature files."""

from pytest_bdd import scenarios

scenarios("../features/api")
