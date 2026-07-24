# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

import contextlib
from unittest.mock import patch

import httpx
import pytest

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


# ---------------------------------------------------------------------------
# Core signing
# ---------------------------------------------------------------------------


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


def test_sign_request_strips_conflicting_headers():
    """Verify SDK credentials are removed before OCI signing."""
    auth = _DummyAuth(_DummySigner("oci-sig"))
    request = httpx.Request(
        "POST",
        "https://example.com/api?key=google-sdk-key&keep=value",
        headers={
            "Authorization": "Bearer sdk-token",
            "X-Api-Key": "sdk-key",
            "x-goog-api-key": "google-sdk-key",
            "Content-Type": "application/json",
        },
        content=b'{"hello": "world"}',
    )
    auth._sign_request(request, request.content, auth.signer)
    assert request.headers["authorization"] == "oci-sig"
    assert "x-api-key" not in request.headers
    assert "x-goog-api-key" not in request.headers
    assert request.headers["content-type"] == "application/json"
    assert request.url.params.get("key") is None
    assert request.url.params.get("keep") == "value"


def test_sign_request_with_body():
    """Verify signing works with POST bodies."""
    auth = _DummyAuth(_DummySigner("oci-sig"))
    body = b'{"model": "grok", "input": "hello"}'
    request = httpx.Request(
        "POST",
        "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1/responses",
        content=body,
    )
    auth._sign_request(request, body, auth.signer)
    assert request.headers["authorization"] == "oci-sig"


# ---------------------------------------------------------------------------
# 401 retry
# ---------------------------------------------------------------------------


def test_auth_flow_refreshes_on_401():
    auth = _DummyAuth(_DummySigner("signed-0"))
    request = httpx.Request("GET", "https://example.com")
    flow = auth.auth_flow(request)
    signed_request = next(flow)
    response = httpx.Response(401, request=signed_request)
    retry_request = flow.send(response)
    assert auth.refresh_calls == 1
    assert retry_request.headers["authorization"] == "signed-1"


def test_auth_flow_no_retry_on_200():
    """Non-401 responses should not trigger a refresh."""
    auth = _DummyAuth(_DummySigner("signed-0"))
    request = httpx.Request("GET", "https://example.com")
    flow = auth.auth_flow(request)
    signed_request = next(flow)
    response = httpx.Response(200, request=signed_request)
    with contextlib.suppress(StopIteration):
        flow.send(response)
    assert auth.refresh_calls == 0


def test_auth_flow_401_refresh_failure_does_not_crash(caplog):
    """When 401 retry refresh fails, the generator should end gracefully
    and the caller receives the original 401 (not a crash)."""
    auth = _BrokenRefreshAuth(_DummySigner("signed-0"), refresh_interval=99999)
    request = httpx.Request("GET", "https://example.com")

    with caplog.at_level("ERROR"):
        flow = auth.auth_flow(request)
        signed_request = next(flow)
        response = httpx.Response(401, request=signed_request)
        with pytest.raises(StopIteration):
            flow.send(response)

    assert auth._last_refresh_error is not None
    assert any("Token refresh on 401 failed" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Scheduled refresh
# ---------------------------------------------------------------------------


def test_refresh_if_needed_calls_refresh_signer():
    auth = _DummyAuth(_DummySigner("signed-0"), refresh_interval=0)
    auth._refresh_if_needed()
    assert auth.refresh_calls == 1


def test_refresh_if_needed_skips_when_interval_not_reached():
    auth = _DummyAuth(_DummySigner("signed-0"), refresh_interval=99999)
    auth._refresh_if_needed()
    assert auth.refresh_calls == 0


def test_refresh_failure_does_not_break_auth_flow(caplog):
    auth = _BrokenRefreshAuth(_DummySigner("signed-0"), refresh_interval=0)
    request = httpx.Request("GET", "https://example.com")

    with caplog.at_level("WARNING"):
        flow = auth.auth_flow(request)
        signed_request = next(flow)

    assert signed_request.headers["authorization"] == "signed-0"
    assert any("Scheduled token refresh failed" in record.message for record in caplog.records)


def test_refresh_failure_tracks_last_error():
    """_last_refresh_error should be set on failure and cleared on success."""
    auth = _BrokenRefreshAuth(_DummySigner("signed-0"), refresh_interval=0)
    auth._refresh_if_needed()
    assert auth._last_refresh_error is not None
    assert isinstance(auth._last_refresh_error, ConnectionError)


def test_refresh_success_clears_error():
    auth = _DummyAuth(_DummySigner("signed-0"), refresh_interval=0)
    auth._last_refresh_error = ConnectionError("old error")
    auth._refresh_if_needed()
    assert auth._last_refresh_error is None
    assert auth.refresh_calls == 1


# ---------------------------------------------------------------------------
# OciSessionAuth
# ---------------------------------------------------------------------------


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


def test_session_auth_missing_key_file():
    config = {
        "security_token_file": "dummy.token",
        "tenancy": "dummy_tenancy",
    }
    with (
        patch("oci.config.from_file", return_value=config),
        patch("builtins.open", create=True) as mock_open,
    ):
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy_token"
        with pytest.raises(KeyError, match="key_file"):
            OciSessionAuth(profile_name="DEFAULT")


def test_session_auth_refresh_reloads_config():
    """Verify refresh re-reads config and token files."""
    config = {
        "key_file": "dummy.key",
        "security_token_file": "dummy.token",
    }
    with (
        patch("oci.config.from_file", return_value=config) as mock_config,
        patch("oci.signer.load_private_key_from_file", return_value="dummy_key"),
        patch("oci.auth.signers.SecurityTokenSigner") as mock_signer,
        patch("builtins.open", create=True) as mock_open,
    ):
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy_token"
        auth = OciSessionAuth(profile_name="TEST")
        initial_calls = mock_config.call_count

        auth._refresh_signer()

        assert mock_config.call_count == initial_calls + 1
        assert mock_signer.call_count == 2


# ---------------------------------------------------------------------------
# OciUserPrincipalAuth
# ---------------------------------------------------------------------------


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


def test_user_principal_auth_refresh_reloads_config():
    config = {
        "key_file": "dummy.key",
        "tenancy": "dummy_tenancy",
        "user": "dummy_user",
        "fingerprint": "dummy_fingerprint",
    }
    with (
        patch("oci.config.from_file", return_value=config) as mock_config,
        patch("oci.config.validate_config", return_value=True),
        patch("oci.signer.Signer") as mock_signer,
    ):
        auth = OciUserPrincipalAuth(profile_name="TEST")
        initial_calls = mock_config.call_count
        auth._refresh_signer()
        assert mock_config.call_count == initial_calls + 1
        assert mock_signer.call_count == 2


# ---------------------------------------------------------------------------
# OciResourcePrincipalAuth / OciInstancePrincipalAuth
# ---------------------------------------------------------------------------


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
