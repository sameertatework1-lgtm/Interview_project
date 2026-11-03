"""BaseClient: wraps Playwright APIRequestContext with logging."""

from __future__ import annotations

import json
from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseClient:
    """Base API client. One subclass per service."""

    def __init__(self, request_context: APIRequestContext, base_url: str) -> None:
        self._ctx = request_context
        self._base_url = base_url.rstrip("/")

    # ── HTTP helpers ──────────────────────────────────────────────────────────

    def _url(self, path: str = "") -> str:
        if not path or path == "/":
            return self._base_url
        if not path.startswith("/"):
            path = "/" + path
        return f"{self._base_url}{path}"

    def _log(self, method: str, url: str, resp: APIResponse, body: Any = None) -> None:
        status = resp.status
        logger.debug("%s %s → %d", method, url, status)
        if status >= 400:
            try:
                payload = resp.json()
            except Exception:
                payload = resp.text()
            logger.warning("Response body: %s", payload)
            with allure.step(f"{method} {url} → {status}"):
                allure.attach(
                    json.dumps(body, indent=2) if body else "no body",
                    name="request_body",
                    attachment_type=allure.attachment_type.JSON,
                )
                allure.attach(
                    json.dumps(payload, indent=2) if isinstance(payload, dict) else str(payload),
                    name="response_body",
                    attachment_type=allure.attachment_type.JSON,
                )

    def get(self, path: str = "", *, token: str | None = None, **kwargs) -> APIResponse:
        url = self._url(path)
        headers = self._auth_header(token)
        resp = self._ctx.get(url, headers=headers, **kwargs)
        self._log("GET", url, resp)
        return resp

    def post(
        self, path: str = "", *, data: dict | None = None, token: str | None = None, **kwargs
    ) -> APIResponse:
        url = self._url(path)
        headers = self._auth_header(token)
        resp = self._ctx.post(
            url, data=json.dumps(data) if data is not None else None, headers=headers, **kwargs
        )
        self._log("POST", url, resp, data)
        return resp

    def put(
        self, path: str = "", *, data: dict | None = None, token: str | None = None, **kwargs
    ) -> APIResponse:
        url = self._url(path)
        headers = self._auth_header(token)
        resp = self._ctx.put(
            url, data=json.dumps(data) if data is not None else None, headers=headers, **kwargs
        )
        self._log("PUT", url, resp, data)
        return resp

    def delete(self, path: str = "", *, token: str | None = None, **kwargs) -> APIResponse:
        url = self._url(path)
        headers = self._auth_header(token)
        resp = self._ctx.delete(url, headers=headers, **kwargs)
        self._log("DELETE", url, resp)
        return resp

    def patch(
        self, path: str = "", *, data: dict | None = None, token: str | None = None, **kwargs
    ) -> APIResponse:
        url = self._url(path)
        headers = self._auth_header(token)
        resp = self._ctx.fetch(
            url,
            method="PATCH",
            data=json.dumps(data) if data is not None else None,
            headers=headers,
            **kwargs,
        )
        self._log("PATCH", url, resp, data)
        return resp

    @staticmethod
    def _auth_header(token: str | None) -> dict:
        base = {"Content-Type": "application/json"}
        if token:
            base["Cookie"] = f"token={token}"
        return base
