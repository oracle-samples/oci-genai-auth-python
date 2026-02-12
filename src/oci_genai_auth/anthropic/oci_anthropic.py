# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from typing import Any, Mapping

import httpx
from anthropic import (
    DEFAULT_MAX_RETRIES,
    NOT_GIVEN,
    AsyncAnthropic,
    DefaultAsyncHttpxClient,
    DefaultHttpxClient,
    NotGiven,
    Omit,
    Timeout,
    omit,
    Anthropic,
)

from ..auth import (  # noqa: F401
    HttpxOciAuth,
    OciInstancePrincipalAuth,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)

COMPARTMENT_ID_HEADER = "CompartmentId"
OPC_COMPARTMENT_ID_HEADER = "opc-compartment-id"


class OciAnthropic(Anthropic):
    """
    OCI-ready wrapper for the Anthropic SDK client.

    This class configures the Anthropic SDK with a custom base URL and
    OCI request signing so you can call Anthropic-style APIs against
    OCI-proxied endpoints.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        base_url: str,
        compartment_id: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str | Omit] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        **kwargs: Any,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required for OciAnthropic.")

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )

        request_headers = _build_headers(compartment_id)
        custom_headers = _merge_headers(default_headers, request_headers)
        custom_headers = _ensure_auth_headers_omitted(custom_headers)

        client = http_client or DefaultHttpxClient(
            auth=auth,
            headers=request_headers,
        )

        super().__init__(
            api_key=None,
            auth_token=None,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=custom_headers,
            default_query=default_query,
            http_client=client,
            **kwargs,
        )


class AsyncOciAnthropic(AsyncAnthropic):
    """
    Async OCI-ready wrapper for the Anthropic SDK client.

    Supports async/await usage while applying OCI request signing and
    OCI headers for Anthropic-compatible endpoints.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        base_url: str,
        compartment_id: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str | Omit] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        **kwargs: Any,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required for AsyncOciAnthropic.")

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )

        request_headers = _build_headers(compartment_id)
        custom_headers = _merge_headers(default_headers, request_headers)
        custom_headers = _ensure_auth_headers_omitted(custom_headers)

        client = http_client or DefaultAsyncHttpxClient(
            auth=auth,
            headers=request_headers,
        )

        super().__init__(
            api_key=None,
            auth_token=None,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=custom_headers,
            default_query=default_query,
            http_client=client,
            **kwargs,
        )


def _build_headers(compartment_id: str | None) -> dict[str, str]:
    if not compartment_id:
        return {}
    return {
        COMPARTMENT_ID_HEADER: compartment_id,
        OPC_COMPARTMENT_ID_HEADER: compartment_id,
    }


def _merge_headers(
    base: Mapping[str, str | Omit] | None,
    extra: Mapping[str, str],
) -> dict[str, str | Omit]:
    merged: dict[str, str | Omit] = {}
    if base:
        merged.update(base)
    for key, value in extra.items():
        merged.setdefault(key, value)
    return merged


def _ensure_auth_headers_omitted(headers: Mapping[str, str | Omit]) -> dict[str, str | Omit]:
    if "X-Api-Key" in headers or "Authorization" in headers:
        return dict(headers)

    updated = dict(headers)
    updated["X-Api-Key"] = omit
    return updated


__all__ = [
    "OciAnthropic",
    "AsyncOciAnthropic",
    "COMPARTMENT_ID_HEADER",
    "OPC_COMPARTMENT_ID_HEADER",
    "HttpxOciAuth",
]
