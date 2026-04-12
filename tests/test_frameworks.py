# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Unit tests for oci_genai_auth.frameworks helpers."""

from __future__ import annotations

import threading
import time
from unittest.mock import MagicMock, patch

import httpx
import pytest

from oci_genai_auth.auth import HttpxOciAuth
from oci_genai_auth.frameworks import (
    _ENDPOINT_TEMPLATE,
    _resolve_auth,
    _validate_region,
    build_async_http_client,
    build_http_client,
)

# ---------------------------------------------------------------------------
# Stub auth (no real OCI credentials needed)
# ---------------------------------------------------------------------------


class _StubAuth(HttpxOciAuth):
    def __init__(self) -> None:
        self.signer = MagicMock()
        self.refresh_interval = 3600
        self._lock = threading.Lock()
        self._last_refresh = time.time()
        self._last_refresh_error = None

    def _refresh_signer(self) -> None:
        pass


# ---------------------------------------------------------------------------
# _validate_region
# ---------------------------------------------------------------------------


def test_validate_region_accepts_valid():
    assert _validate_region("us-chicago-1") == "us-chicago-1"
    assert _validate_region("eu-frankfurt-1") == "eu-frankfurt-1"
    assert _validate_region("ap-tokyo-1") == "ap-tokyo-1"
    assert _validate_region("ca-toronto-1") == "ca-toronto-1"


def test_validate_region_rejects_invalid():
    with pytest.raises(ValueError, match="Invalid OCI region"):
        _validate_region("evil.com/foo")
    with pytest.raises(ValueError, match="Invalid OCI region"):
        _validate_region("")
    with pytest.raises(ValueError, match="Invalid OCI region"):
        _validate_region("us-chicago")
    with pytest.raises(ValueError, match="Invalid OCI region"):
        _validate_region("US-CHICAGO-1")


# ---------------------------------------------------------------------------
# _resolve_auth
# ---------------------------------------------------------------------------


def test_resolve_auth_returns_provided_auth():
    auth = _StubAuth()
    assert _resolve_auth(auth) is auth


def test_resolve_auth_creates_session_auth_by_default():
    with patch("oci_genai_auth.frameworks.OciSessionAuth") as mock_cls:
        mock_cls.return_value = _StubAuth()
        result = _resolve_auth(profile_name="TEST")
        mock_cls.assert_called_once_with(profile_name="TEST")
        assert result is mock_cls.return_value


def test_resolve_auth_creates_user_principal_auth():
    with patch("oci_genai_auth.frameworks.OciUserPrincipalAuth") as mock_cls:
        mock_cls.return_value = _StubAuth()
        result = _resolve_auth(profile_name="TEST", auth_type="user_principal")
        mock_cls.assert_called_once_with(profile_name="TEST")
        assert result is mock_cls.return_value


def test_resolve_auth_passes_config_file():
    with patch("oci_genai_auth.frameworks.OciSessionAuth") as mock_cls:
        mock_cls.return_value = _StubAuth()
        _resolve_auth(profile_name="X", config_file="/custom/config")
        mock_cls.assert_called_once_with(profile_name="X", config_file="/custom/config")


# ---------------------------------------------------------------------------
# build_http_client
# ---------------------------------------------------------------------------


def test_build_http_client_sets_project_header():
    auth = _StubAuth()
    client = build_http_client(project_ocid="ocid1.project.test", auth=auth)
    assert isinstance(client, httpx.Client)
    assert client.headers["openai-project"] == "ocid1.project.test"
    client.close()


def test_build_http_client_sets_compartment_header():
    auth = _StubAuth()
    client = build_http_client(
        project_ocid="ocid1.project.test",
        compartment_id="ocid1.compartment.test",
        auth=auth,
    )
    assert client.headers["opc-compartment-id"] == "ocid1.compartment.test"
    client.close()


def test_build_http_client_extra_headers():
    auth = _StubAuth()
    client = build_http_client(
        project_ocid="ocid1.project.test",
        auth=auth,
        extra_headers={"X-Custom": "value"},
    )
    assert client.headers["x-custom"] == "value"
    client.close()


def test_build_http_client_no_compartment_when_none():
    auth = _StubAuth()
    client = build_http_client(project_ocid="ocid1.project.test", auth=auth)
    assert "opc-compartment-id" not in client.headers
    client.close()


# ---------------------------------------------------------------------------
# build_async_http_client
# ---------------------------------------------------------------------------


def test_build_async_http_client_sets_project_header():
    auth = _StubAuth()
    client = build_async_http_client(project_ocid="ocid1.project.test", auth=auth)
    assert isinstance(client, httpx.AsyncClient)
    assert client.headers["openai-project"] == "ocid1.project.test"


# ---------------------------------------------------------------------------
# Framework import errors
# ---------------------------------------------------------------------------


def test_langchain_import_error():
    auth = _StubAuth()
    with patch.dict("sys.modules", {"langchain_openai": None}):
        from oci_genai_auth.frameworks import build_langchain_chat

        with pytest.raises(ImportError, match="langchain-openai"):
            build_langchain_chat(
                model="test",
                project_ocid="ocid1.test",
                auth=auth,
            )


def test_pydantic_ai_import_error():
    auth = _StubAuth()
    with patch.dict(
        "sys.modules",
        {
            "pydantic_ai": None,
            "pydantic_ai.models": None,
            "pydantic_ai.models.openai": None,
        },
    ):
        from oci_genai_auth.frameworks import build_pydantic_ai_model

        with pytest.raises(ImportError, match="pydantic-ai"):
            build_pydantic_ai_model(
                model="test",
                project_ocid="ocid1.test",
                auth=auth,
            )


def test_agents_import_error():
    auth = _StubAuth()
    with patch.dict("sys.modules", {"agents": None}):
        from oci_genai_auth.frameworks import configure_openai_agents

        with pytest.raises(ImportError, match="openai-agents"):
            configure_openai_agents(
                project_ocid="ocid1.test",
                auth=auth,
            )


# ---------------------------------------------------------------------------
# Endpoint template
# ---------------------------------------------------------------------------


def test_endpoint_template_format():
    url = _ENDPOINT_TEMPLATE.format(region="us-chicago-1")
    assert url == "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1"
