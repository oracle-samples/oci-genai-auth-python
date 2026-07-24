# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Shared configuration for OCI Generative AI SDK examples."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import httpx

from oci_genai_auth import OciSessionAuth

if TYPE_CHECKING:
    from google import genai
    from openai import AsyncOpenAI, OpenAI

# Shared defaults.
PROFILE_NAME = os.getenv("OCI_GENAI_PROFILE", "DEFAULT")
COMPARTMENT_ID = os.getenv("OCI_GENAI_COMPARTMENT_ID", "")
PROJECT_OCID = os.getenv("OCI_GENAI_PROJECT_ID", "<<ENTER_PROJECT_ID>>")
REGION = os.getenv("OCI_GENAI_REGION", "us-chicago-1")

OPENAI_BASE_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1"
GOOGLE_BASE_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/google"


def _build_headers(require_compartment_id: bool = False) -> dict[str, str]:
    headers: dict[str, str] = {}
    if COMPARTMENT_ID:
        headers["CompartmentId"] = COMPARTMENT_ID
        headers["opc-compartment-id"] = COMPARTMENT_ID
    elif require_compartment_id:
        raise ValueError("Set OCI_GENAI_COMPARTMENT_ID before running Chat Completions examples.")
    return headers


def build_api_key_openai_client() -> "OpenAI":
    from openai import OpenAI

    return OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=os.getenv("OPENAI_API_KEY"),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
    )


def build_api_key_async_openai_client() -> "AsyncOpenAI":
    from openai import AsyncOpenAI

    return AsyncOpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=os.getenv("OPENAI_API_KEY"),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
    )


def build_oci_iam_openai_client(include_compartment_headers: bool = False) -> "OpenAI":
    from openai import OpenAI

    return OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.Client(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=(
                _build_headers(require_compartment_id=True) if include_compartment_headers else {}
            ),
        ),
    )


def build_oci_iam_async_openai_client(include_compartment_headers: bool = False) -> "AsyncOpenAI":
    from openai import AsyncOpenAI

    return AsyncOpenAI(
        base_url=OPENAI_BASE_URL,
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.AsyncClient(
            auth=OciSessionAuth(profile_name=PROFILE_NAME),
            headers=(
                _build_headers(require_compartment_id=True) if include_compartment_headers else {}
            ),
        ),
    )


def build_api_key_google_client() -> "genai.Client":
    """Build a Google Gen AI client using an OCI Generative AI API key."""
    from google import genai

    api_key = os.getenv("OCI_GENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OCI_GENAI_API_KEY before running this example.")
    return genai.Client(api_key=api_key, http_options={"base_url": GOOGLE_BASE_URL})


def build_oci_iam_google_client() -> "genai.Client":
    """Build a Google Gen AI client that signs requests with OCI IAM."""
    from google import genai

    headers = _build_headers()
    return genai.Client(
        api_key="not-used",
        http_options={
            "base_url": GOOGLE_BASE_URL,
            "headers": headers,
            "httpx_client": httpx.Client(
                auth=OciSessionAuth(profile_name=PROFILE_NAME), headers=headers
            ),
        },
    )


def build_oci_iam_async_google_client() -> tuple["genai.Client", "httpx.AsyncClient"]:
    """Build an async Google Gen AI client that signs requests with OCI IAM."""
    from google import genai

    headers = _build_headers()
    http_client = httpx.AsyncClient(auth=OciSessionAuth(profile_name=PROFILE_NAME), headers=headers)
    return (
        genai.Client(
            api_key="not-used",
            http_options={
                "base_url": GOOGLE_BASE_URL,
                "headers": headers,
                "httpx_async_client": http_client,
            },
        ),
        http_client,
    )
