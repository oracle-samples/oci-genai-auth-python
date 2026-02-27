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
OVERRIDE_URL = ""
PROFILE_NAME = "DEFAULT"
REGION = "us-chicago-1"
GEMINI_API_KEY = ""
GEMINI_BASE_URL = ""


def _build_headers(include_conversation_store_id: bool = False) -> dict[str, str]:
    headers: dict[str, str] = {}
    if COMPARTMENT_ID:
        headers["CompartmentId"] = COMPARTMENT_ID
        headers["opc-compartment-id"] = COMPARTMENT_ID
    if OPENAI_PROJECT:
        headers["OpenAI-Project"] = OPENAI_PROJECT
    if include_conversation_store_id and CONVERSATION_STORE_ID:
        headers["opc-conversation-store-id"] = CONVERSATION_STORE_ID
    return headers


def _resolve_openai_base_url() -> str:
    service_endpoint = OVERRIDE_URL or (
        f"https://inference.generativeai.{REGION}.oci.oraclecloud.com" if REGION else ""
    )
    if not service_endpoint:
        raise ValueError("REGION or OVERRIDE_URL must be set.")
    return f"{service_endpoint.rstrip(' /')}/openai/v1"


def _resolve_anthropic_base_url() -> str:
    if not REGION:
        raise ValueError("REGION or ANTHROPIC_BASE_URL must be set.")
    return f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/anthropic"


def _resolve_google_base_url() -> str:
    if not REGION:
        raise ValueError("REGION or GOOGLE_BASE_URL must be set.")
    return f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/google"


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
        base_url=_resolve_anthropic_base_url(),
        http_client=httpx.Client(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=_build_headers(),
        ),
    )


def build_anthropic_async_client() -> "AsyncAnthropic":
    from anthropic import AsyncAnthropic

    return AsyncAnthropic(
        api_key="not-used",
        base_url=_resolve_anthropic_base_url(),
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
            "base_url": _resolve_google_base_url(),
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
            "base_url": _resolve_google_base_url(),
            "headers": headers,
            "httpx_async_client": http_client,
        },
    )
    return client, http_client
