# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates the Common example."""

import os

import httpx
from oci_genai_support.openai.oci_openai import OPC_COMPARTMENT_ID_HEADER
from openai import AsyncOpenAI, OpenAI

from oci_genai_auth import OciSessionAuth

"""
Common clients used by examples.

- AgentHub (non-pass-through) provide build_openai_agenthub_client (DP)
        and build_openai_agenthub_cp_client (CP).
- Partner (pass-through) examples use `build_openai_client` helpers.
"""

# Shared defaults.
PROFILE_NAME = "DEFAULT"
COMPARTMENT_ID = "<<ENTER_COMPARTMENT_ID>>"
PROJECT_OCID = "<<ENTER_PROJECT_ID>>"

REGION = "us-chicago-1"

# Partner (pass-through) base URL.
PARTNER_OPENAI_BASE_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/v1"

# AgentHub (non-pass-through) base URLs.
AGENTHUB_OPENAI_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1"
AGENTHUB_OPENAI_CP_URL = f"https://generativeai.{REGION}.oci.oraclecloud.com/20231130/openai/v1"


def build_openai_agenthub_client():
    return OpenAI(
        base_url=AGENTHUB_OPENAI_URL,
        api_key=os.getenv("OCI_GENAI_API_KEY", "not-used"),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    )


def build_openai_agenthub_cp_client():
    return OpenAI(
        base_url=AGENTHUB_OPENAI_CP_URL,
        api_key=os.getenv("OCI_GENAI_API_KEY", "not-used"),
        http_client=httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        default_headers={OPC_COMPARTMENT_ID_HEADER: COMPARTMENT_ID},
    )


def build_openai_agenthub_async_client():
    return AsyncOpenAI(
        base_url=AGENTHUB_OPENAI_URL,
        api_key=os.getenv("OCI_GENAI_API_KEY", "not-used"),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.AsyncClient(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    )


def build_openai_pt_client() -> OpenAI:
    client_kwargs = {
        "api_key": "not-used",
        "base_url": PARTNER_OPENAI_BASE_URL,
        "http_client": httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    }
    if COMPARTMENT_ID:
        client_kwargs["default_headers"] = {"opc-compartment-id": COMPARTMENT_ID}
    return OpenAI(**client_kwargs)


def build_openai_pt_async_client() -> AsyncOpenAI:
    client_kwargs = {
        "api_key": "not-used",
        "base_url": PARTNER_OPENAI_BASE_URL,
        "http_client": httpx.AsyncClient(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    }
    if COMPARTMENT_ID:
        client_kwargs["default_headers"] = {"opc-compartment-id": COMPARTMENT_ID}
    return AsyncOpenAI(**client_kwargs)
