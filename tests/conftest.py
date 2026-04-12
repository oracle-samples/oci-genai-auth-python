# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Shared fixtures for both unit and integration tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Global: disable noisy tracing from OpenAI Agents SDK
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True, scope="session")
def _disable_openai_agents_tracing():
    os.environ.setdefault("OPENAI_AGENTS_DISABLE_TRACING", "true")
    try:
        from agents.tracing import set_tracing_disabled
    except (ImportError, ModuleNotFoundError):
        yield
        return
    set_tracing_disabled(True)
    yield


# ---------------------------------------------------------------------------
# Integration test environment
# ---------------------------------------------------------------------------

def _load_env():
    """Load tests/.env if present (plain KEY=VALUE, no shell expansion)."""
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key:
            os.environ.setdefault(key, value)


_load_env()


# Required env vars for integration tests
_REQUIRED_VARS = (
    "OCI_GENAI_PROJECT_ID",
    "OCI_GENAI_REGION",
    "OCI_GENAI_MODEL",
    "OCI_GENAI_PROFILE",
    "OCI_GENAI_AUTH_TYPE",
)


def _env(var: str) -> str:
    return os.environ.get(var, "")


def _integration_configured() -> bool:
    """Return True if all required env vars are set to non-placeholder values."""
    return all(
        _env(v) and "example" not in _env(v).lower()
        for v in _REQUIRED_VARS
    )


# Marker: skip integration tests when env is not configured
requires_oci = pytest.mark.skipif(
    not _integration_configured(),
    reason="Integration tests require OCI_GENAI_* env vars (see tests/.env.example)",
)


@pytest.fixture(scope="session")
def oci_project_id():
    return _env("OCI_GENAI_PROJECT_ID")


@pytest.fixture(scope="session")
def oci_compartment_id():
    return _env("OCI_GENAI_COMPARTMENT_ID")


@pytest.fixture(scope="session")
def oci_region():
    return _env("OCI_GENAI_REGION")


@pytest.fixture(scope="session")
def oci_model():
    return _env("OCI_GENAI_MODEL")


@pytest.fixture(scope="session")
def oci_profile():
    return _env("OCI_GENAI_PROFILE")


@pytest.fixture(scope="session")
def oci_auth_type():
    return _env("OCI_GENAI_AUTH_TYPE")
