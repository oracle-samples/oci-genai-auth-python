# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from oci_genai_auth import OciSessionAuth

if TYPE_CHECKING:
    from anthropic import Anthropic, AsyncAnthropic
    from google import genai
    from openai import AsyncOpenAI, OpenAI

# Fill in these values for tests
COMPARTMENT_ID = ""
CONVERSATION_STORE_ID = ""
OPENAI_PROJECT = ""
PROFILE_NAME = "DEFAULT"
GEMINI_API_KEY = ""

# OpenAI-compatible base URLs.
OPENAI_BASE_URL_PT = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/v1"
OPENAI_BASE_URL_NP = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1"
# Switch to "NP" for examples that store data on the server.
RESPONSE_API_MODE = "PT"  # "PT" (pass-through) or "NP" (non-pass-through)

# Other provider base URLs.
ANTHROPIC_BASE_URL = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/anthropic"
GOOGLE_BASE_URL = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/google"


def _build_headers(include_conversation_store_id: bool = False) -> dict[str, str]:
    headers: dict[str, str] = {
        "CompartmentId": COMPARTMENT_ID,
        "opc-compartment-id": COMPARTMENT_ID,
        "OpenAI-Project": OPENAI_PROJECT,
    }
    if include_conversation_store_id:
        headers["opc-conversation-store-id"] = CONVERSATION_STORE_ID
    return {key: value for key, value in headers.items() if value}


def _resolve_openai_base_url() -> str:
    return OPENAI_BASE_URL_NP if RESPONSE_API_MODE == "NP" else OPENAI_BASE_URL_PT


def build_openai_client() -> "OpenAI":
    from openai import OpenAI

    client_kwargs = {
        "api_key": "not-used",
        "base_url": _resolve_openai_base_url(),
        "http_client": httpx.Client(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=_build_headers(include_conversation_store_id=True),
        ),
    }
    if OPENAI_PROJECT:
        client_kwargs["project"] = OPENAI_PROJECT
    return OpenAI(**client_kwargs)


def build_openai_async_client() -> "AsyncOpenAI":
    from openai import AsyncOpenAI

    client_kwargs = {
        "api_key": "not-used",
        "base_url": _resolve_openai_base_url(),
        "http_client": httpx.AsyncClient(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=_build_headers(include_conversation_store_id=True),
        ),
    }
    if OPENAI_PROJECT:
        client_kwargs["project"] = OPENAI_PROJECT
    return AsyncOpenAI(**client_kwargs)


def build_anthropic_client() -> "Anthropic":
    from anthropic import Anthropic

    return Anthropic(
        api_key="not-used",
        base_url=ANTHROPIC_BASE_URL,
        http_client=httpx.Client(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=_build_headers(),
        ),
    )


def build_anthropic_async_client() -> "AsyncAnthropic":
    from anthropic import AsyncAnthropic

    return AsyncAnthropic(
        api_key="not-used",
        base_url=ANTHROPIC_BASE_URL,
        http_client=httpx.AsyncClient(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=_build_headers(),
        ),
    )


def build_google_client() -> "genai.Client":
    from google import genai

    headers = _build_headers()
    http_client = httpx.Client(
        auth=OciSessionAuth(profile_name=PROFILE_NAME),
        headers=headers,
    )
    return genai.Client(
        api_key="not-used",
        http_options={
            "base_url": GOOGLE_BASE_URL,
            "headers": headers,
            "httpx_client": http_client,
        },
    )


def build_google_async_client() -> tuple["genai.Client", httpx.AsyncClient]:
    from google import genai

    headers = _build_headers()
    http_client = httpx.AsyncClient(
        auth=OciSessionAuth(profile_name=PROFILE_NAME),
        headers=headers,
    )
    client = genai.Client(
        api_key="not-used",
        http_options={
            "base_url": GOOGLE_BASE_URL,
            "headers": headers,
            "httpx_async_client": http_client,
        },
    )
    return client, http_client
