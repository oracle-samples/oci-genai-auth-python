# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""AgentHub example clients and configuration."""

from __future__ import annotations

import os

import httpx
from openai import AsyncOpenAI, OpenAI

from oci_genai_auth import OciSessionAuth

# Shared defaults.
PROFILE_NAME = "DEFAULT"
COMPARTMENT_ID = "<<ENTER_COMPARTMENT_ID>>"
PROJECT_OCID = "<<ENTER_PROJECT_ID>>"
REGION = "us-chicago-1"

AGENTHUB_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1"
AGENTHUB_CP_URL = f"https://generativeai.{REGION}.oci.oraclecloud.com/20231130/openai/v1"


def build_agenthub_client() -> OpenAI:
    return OpenAI(
        base_url=AGENTHUB_URL,
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    )


def build_agenthub_async_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=AGENTHUB_URL,
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        http_client=httpx.AsyncClient(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
    )


def build_agenthub_cp_client() -> OpenAI:
    return OpenAI(
        base_url=AGENTHUB_CP_URL,
        api_key="not-used",
        http_client=httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        default_headers={"opc-compartment-id": COMPARTMENT_ID},
    )