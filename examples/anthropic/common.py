# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

import os

from oci_genai_auth import OciSessionAuth
from oci_genai_auth.anthropic import OciAnthropic


def build_client() -> OciAnthropic:
    client = OciAnthropic(
        auth=OciSessionAuth(profile_name="DEFAULT"),
        base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/anthropic",
        compartment_id="<???>",
    )
    return client


def get_model(default: str = "claude-sonnet-4-5") -> str:
    return os.getenv("ANTHROPIC_MODEL", default)
