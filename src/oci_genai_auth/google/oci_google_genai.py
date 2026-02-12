# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from typing import Any, Mapping

import httpx
from google import genai
from google.genai import types

from ..auth import HttpxOciAuth  # noqa: F401

COMPARTMENT_ID_HEADER = "CompartmentId"


class OciGoogleGenAI:
    """
    OCI-ready wrapper for the Google Gen AI SDK client.

    This class configures the Google Gen AI SDK with a custom base URL and
    OCI request signing so you can call generateContent / generateImage style APIs
    against OCI-proxied endpoints.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth | None,
        base_url: str,
        compartment_id: str | None = None,
        headers: Mapping[str, str] | None = None,
        http_options: types.HttpOptions | Mapping[str, Any] | None = None,
        vertexai: bool = True,
        project: str | None = None,
        location: str | None = None,
        **kwargs: Any,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required for OciGoogleGenAI.")

        request_headers = _build_headers(compartment_id, headers)
        merged_http_options = _merge_http_options(base_url, auth, request_headers, http_options)

        client_kwargs: dict[str, Any] = {
            "vertexai": vertexai,
            "http_options": merged_http_options,
        }
        if project is not None:
            client_kwargs["project"] = project
        if location is not None:
            client_kwargs["location"] = location
        client_kwargs.update(kwargs)

        self._client = genai.Client(**client_kwargs)

    @property
    def client(self) -> genai.Client:
        return self._client

    def generate_content(self, model: str, contents: Any, **kwargs: Any) -> Any:
        return self._client.models.generate_content(model=model, contents=contents, **kwargs)

    def generate_images(self, model: str, prompt: str, **kwargs: Any) -> Any:
        return self._client.models.generate_images(model=model, prompt=prompt, **kwargs)

    def generate_image(self, model: str, prompt: str, **kwargs: Any) -> Any:
        return self.generate_images(model=model, prompt=prompt, **kwargs)


def _build_headers(
    compartment_id: str | None,
    headers: Mapping[str, str] | None,
) -> dict[str, str]:
    request_headers: dict[str, str] = {}
    if headers:
        request_headers.update(headers)
    if compartment_id and COMPARTMENT_ID_HEADER not in request_headers:
        request_headers[COMPARTMENT_ID_HEADER] = compartment_id
    return request_headers


def _merge_http_options(
    base_url: str,
    auth: httpx.Auth | None,
    headers: Mapping[str, str],
    http_options: types.HttpOptions | Mapping[str, Any] | None,
) -> types.HttpOptions:
    if http_options is None:
        options: dict[str, Any] = {}
    elif isinstance(http_options, types.HttpOptions):
        options = http_options.model_dump(exclude_none=True)
    else:
        options = dict(http_options)

    options["base_url"] = base_url

    merged_headers: dict[str, str] = {}
    merged_headers.update(options.get("headers", {}) or {})
    merged_headers.update(headers)
    if merged_headers:
        options["headers"] = merged_headers

    client_args = dict(options.get("client_args", {}) or {})
    async_client_args = dict(options.get("async_client_args", {}) or {})
    if auth is not None:
        client_args.setdefault("auth", auth)
        async_client_args.setdefault("auth", auth)
    # Preserve empty dicts so callers can reliably inspect for "auth".
    options["client_args"] = client_args
    options["async_client_args"] = async_client_args

    return types.HttpOptions(**options)


__all__ = [
    "OciGoogleGenAI",
    "COMPARTMENT_ID_HEADER",
    "HttpxOciAuth",
]
