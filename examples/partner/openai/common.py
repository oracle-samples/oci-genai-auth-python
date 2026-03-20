# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Partner (pass-through) example clients and configuration."""

from __future__ import annotations

import httpx
from openai import AsyncOpenAI, OpenAI

from oci_genai_auth import OciSessionAuth

PROFILE_NAME = "DEFAULT"
COMPARTMENT_ID = "<<ENTER_COMPARTMENT_ID>>"
REGION = "us-chicago-1"

PARTNER_OPENAI_BASE_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/v1"


def build_openai_client() -> OpenAI:
    client_kwargs = {
        "api_key": "not-used",
        "base_url": PARTNER_OPENAI_BASE_URL,
        "http_client": httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    }
    if COMPARTMENT_ID:
        client_kwargs["default_headers"] = {"opc-compartment-id": COMPARTMENT_ID}
    return OpenAI(**client_kwargs)


def build_openai_async_client() -> AsyncOpenAI:
    client_kwargs = {
        "api_key": "not-used",
        "base_url": PARTNER_OPENAI_BASE_URL,
        "http_client": httpx.AsyncClient(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    }
    if COMPARTMENT_ID:
        client_kwargs["default_headers"] = {"opc-compartment-id": COMPARTMENT_ID}
    return AsyncOpenAI(**client_kwargs)
