import httpx
import pytest


class DummyAuth(httpx.Auth):
    def auth_flow(self, request):  # type: ignore[override]
        yield request


def test_builds_http_client_and_headers():
    pytest.importorskip("anthropic")
    from anthropic import Omit
    from oci_genai_auth.anthropic import (
        COMPARTMENT_ID_HEADER,
        OPC_COMPARTMENT_ID_HEADER,
        OciAnthropic,
    )

    auth = DummyAuth()
    client = OciAnthropic(
        auth=auth,
        base_url="https://example.com",
        compartment_id="ocid1.compartment.oc1..dummy",
        default_headers={"X-Test": "1"},
    )

    assert client._client.auth is auth
    assert client._client.headers[COMPARTMENT_ID_HEADER] == "ocid1.compartment.oc1..dummy"
    assert client._client.headers[OPC_COMPARTMENT_ID_HEADER] == "ocid1.compartment.oc1..dummy"
    assert client.default_headers["X-Test"] == "1"
    assert isinstance(client.default_headers.get("X-Api-Key"), Omit)


def test_async_client_builds_http_client():
    pytest.importorskip("anthropic")
    from oci_genai_auth.anthropic import AsyncOciAnthropic

    auth = DummyAuth()
    client = AsyncOciAnthropic(
        auth=auth,
        base_url="https://example.com",
    )

    assert client._client.auth is auth
