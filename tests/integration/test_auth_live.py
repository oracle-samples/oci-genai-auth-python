# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Live integration tests for OCI auth classes.

These tests make real API calls to the OCI Enterprise AI Agents endpoint
to verify that request signing works end-to-end.  They are skipped
automatically when ``OCI_GENAI_*`` environment variables are not set
(see ``tests/.env.example``).

The assertions verify that:
  - The request was accepted (not 401/403/404)
  - A non-empty response was returned
  - OCI signing headers replaced SDK-injected headers

They intentionally do NOT assert on response content (model output is
non-deterministic). The goal is to verify auth, not model behavior.
"""

from __future__ import annotations

import httpx
from openai import AsyncOpenAI, OpenAI

from oci_genai_auth import OciSessionAuth, OciUserPrincipalAuth
from tests.conftest import requires_oci

_ENDPOINT = "https://inference.generativeai.{region}.oci.oraclecloud.com/openai/v1"


def _build_auth(profile: str, auth_type: str):
    """Create the appropriate auth instance based on env config."""
    if auth_type == "user_principal":
        return OciUserPrincipalAuth(profile_name=profile)
    return OciSessionAuth(profile_name=profile)


@requires_oci
class TestOciAuthSigningLive:
    """Verify that OCI request signing produces valid, accepted requests."""

    def test_sync_responses_api(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        """Sign a sync request and verify the Responses API accepts it."""
        auth = _build_auth(oci_profile, oci_auth_type)
        client = OpenAI(
            base_url=_ENDPOINT.format(region=oci_region),
            api_key="not-used",
            project=oci_project_id,
            http_client=httpx.Client(auth=auth),
        )
        resp = client.responses.create(
            model=oci_model,
            input="What is 2+2?",
            store=False,
        )
        assert resp.output_text, "Expected non-empty response from Responses API"

    def test_async_responses_api(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        """Sign an async request and verify the Responses API accepts it."""
        import asyncio

        auth = _build_auth(oci_profile, oci_auth_type)

        async def _run():
            client = AsyncOpenAI(
                base_url=_ENDPOINT.format(region=oci_region),
                api_key="not-used",
                project=oci_project_id,
                http_client=httpx.AsyncClient(auth=auth),
            )
            resp = await client.responses.create(
                model=oci_model,
                input="What is 2+2?",
                store=False,
            )
            return resp.output_text

        output = asyncio.run(_run())
        assert output, "Expected non-empty response from async Responses API"

    def test_raw_httpx_request(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        """Verify signing works at the raw httpx level (no OpenAI SDK)."""
        auth = _build_auth(oci_profile, oci_auth_type)
        client = httpx.Client(auth=auth)

        url = _ENDPOINT.format(region=oci_region) + "/responses"
        body = {
            "model": oci_model,
            "input": "What is 2+2?",
            "store": False,
        }
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Project": oci_project_id,
        }
        resp = client.post(url, json=body, headers=headers, timeout=60)

        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        # Response must contain output (either output_text or output array)
        assert data.get("output_text") or data.get(
            "output"
        ), "Expected non-empty output in response"

    def test_auth_headers_stripped(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
    ):
        """Verify that sdk-injected Authorization/X-Api-Key headers are
        replaced by OCI signing headers, not sent alongside them."""
        auth = _build_auth(oci_profile, oci_auth_type)
        request = httpx.Request(
            "GET",
            _ENDPOINT.format(region=oci_region) + "/responses",
            headers={
                "Authorization": "Bearer should-be-stripped",
                "X-Api-Key": "should-be-stripped",
            },
        )
        flow = auth.auth_flow(request)
        signed = next(flow)

        # OCI signing should have replaced Authorization
        assert signed.headers["authorization"] != "Bearer should-be-stripped"
        assert signed.headers["authorization"].startswith("Signature ")
        # X-Api-Key should be gone
        assert "x-api-key" not in signed.headers
