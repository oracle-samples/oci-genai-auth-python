# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from unittest.mock import patch

import httpx

from oci_genai_auth.auth import (
    HttpxOciAuth,
    OciInstancePrincipalAuth,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)


class _DummySigner:
    def __init__(self, token: str) -> None:
        self.token = token

    def do_request_sign(self, prepared_request) -> None:  # noqa: ANN001
        prepared_request.headers["authorization"] = self.token


class _DummyAuth(HttpxOciAuth):
    def __init__(self, signer: _DummySigner, refresh_interval: int = 3600) -> None:
        self.refresh_calls = 0
        super().__init__(signer=signer, refresh_interval=refresh_interval)

    def _refresh_signer(self) -> None:
        self.refresh_calls += 1
        self.signer = _DummySigner(f"signed-{self.refresh_calls}")


class _BrokenRefreshAuth(HttpxOciAuth):
    def _refresh_signer(self) -> None:
        raise ConnectionError("metadata service unreachable")


def test_auth_flow_signs_request():
    auth = _DummyAuth(_DummySigner("signed-0"))
    request = httpx.Request(
        "GET",
        "https://example.com?foo=bar",
        headers={
            "Authorization": "Bearer test",
            "X-Api-Key": "api-key",
        },
    )
    flow = auth.auth_flow(request)
    signed_request = next(flow)
    assert signed_request.headers["authorization"] == "signed-0"
    assert "x-api-key" not in signed_request.headers
    assert signed_request.url.params.get("foo") == "bar"


def test_auth_flow_refreshes_on_401():
    auth = _DummyAuth(_DummySigner("signed-0"))
    request = httpx.Request("GET", "https://example.com")
    flow = auth.auth_flow(request)
    signed_request = next(flow)
    response = httpx.Response(401, request=signed_request)
    retry_request = flow.send(response)
    assert auth.refresh_calls == 1
    assert retry_request.headers["authorization"] == "signed-1"


def test_refresh_if_needed_calls_refresh_signer():
    auth = _DummyAuth(_DummySigner("signed-0"), refresh_interval=0)
    auth._refresh_if_needed()
    assert auth.refresh_calls == 1


def test_refresh_failure_does_not_break_auth_flow(caplog):
    auth = _BrokenRefreshAuth(_DummySigner("signed-0"), refresh_interval=0)
    request = httpx.Request("GET", "https://example.com")

    with caplog.at_level("ERROR"):
        flow = auth.auth_flow(request)
        signed_request = next(flow)

    assert signed_request.headers["authorization"] == "signed-0"
    assert any("Token refresh failed" in record.message for record in caplog.records)


def test_session_auth_initializes_signer_from_config():
    config = {
        "key_file": "dummy.key",
        "security_token_file": "dummy.token",
        "tenancy": "dummy_tenancy",
        "user": "dummy_user",
        "fingerprint": "dummy_fingerprint",
    }
    with (
        patch("oci.config.from_file", return_value=config),
        patch("oci.signer.load_private_key_from_file", return_value="dummy_private_key"),
        patch("oci.auth.signers.SecurityTokenSigner") as mock_signer,
        patch("builtins.open", create=True) as mock_open,
    ):
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy_token"
        auth = OciSessionAuth(
            profile_name="DEFAULT",
            generic_headers=["date"],
            body_headers=["content-length"],
        )

    mock_signer.assert_called_once_with(
        "dummy_token",
        "dummy_private_key",
        generic_headers=["date"],
        body_headers=["content-length"],
    )
    assert auth.signer == mock_signer.return_value


def test_user_principal_auth_uses_signer_from_config():
    config = {
        "key_file": "dummy.key",
        "tenancy": "dummy_tenancy",
        "user": "dummy_user",
        "fingerprint": "dummy_fingerprint",
    }
    with (
        patch("oci.config.from_file", return_value=config),
        patch("oci.config.validate_config", return_value=True),
        patch("oci.signer.Signer") as mock_signer,
    ):
        auth = OciUserPrincipalAuth(profile_name="DEFAULT")

    mock_signer.assert_called_once()
    assert auth.signer == mock_signer.return_value


def test_resource_principal_refreshes_signer():
    with patch(
        "oci.auth.signers.get_resource_principals_signer", return_value="signer-1"
    ) as mock_signer:
        auth = OciResourcePrincipalAuth()
        assert auth.signer == "signer-1"
        mock_signer.assert_called_once()

        mock_signer.reset_mock()
        mock_signer.return_value = "signer-2"
        auth._refresh_signer()
        mock_signer.assert_called_once()
        assert auth.signer == "signer-2"


def test_instance_principal_refreshes_signer():
    with patch(
        "oci.auth.signers.InstancePrincipalsSecurityTokenSigner", return_value="signer-1"
    ) as mock_signer:
        auth = OciInstancePrincipalAuth()
        assert auth.signer == "signer-1"
        mock_signer.assert_called_once()

        mock_signer.reset_mock()
        mock_signer.return_value = "signer-2"
        auth._refresh_signer()
        mock_signer.assert_called_once()
        assert auth.signer == "signer-2"
