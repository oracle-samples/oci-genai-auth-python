# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Framework integration helpers for OCI Enterprise AI Agents.

OCI Enterprise AI Agents documentation [1] lists several AI frameworks as
compatible, but none of them work out of the box because:

  1. The ``/openai/v1`` endpoint requires an ``OpenAI-Project`` header with
     the GenAI Project OCID.  No framework besides the raw OpenAI SDK
     exposes a ``project`` parameter.

  2. OCI IAM authentication requires a custom ``httpx.Auth`` handler to sign
     every request.  Only frameworks that accept a custom ``http_client``
     can use it.

This module provides one-liner builder functions that handle both issues
for every framework that supports custom HTTP clients via its public API.

Supported frameworks:
  - OpenAI SDK (``openai``)
  - OpenAI Agents SDK (``openai-agents``)
  - LangChain / LangGraph (``langchain-openai``)
  - PydanticAI (``pydantic-ai``)

Each builder returns a ready-to-use framework client wired to the OCI
endpoint with proper signing and headers.  Framework packages are optional
dependencies -- import errors are deferred to call time.

[1] https://docs.oracle.com/en-us/iaas/Content/generative-ai/oci-openai.htm
"""

from __future__ import annotations

import os
import re
from typing import Any, Optional

import httpx

from .auth import HttpxOciAuth, OciSessionAuth, OciUserPrincipalAuth

__all__ = [
    "build_async_http_client",
    "build_http_client",
    "build_langchain_chat",
    "build_openai_async_client",
    "build_openai_client",
    "build_pydantic_ai_model",
    "configure_openai_agents",
]

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

_ENDPOINT_TEMPLATE = "https://inference.generativeai.{region}.oci.oraclecloud.com/openai/v1"

_REGION_PATTERN = re.compile(r"^[a-z]{2}-[a-z]+-[0-9]+$")


def _validate_region(region: str) -> str:
    """Validate that *region* looks like a legitimate OCI region identifier.

    OCI regions follow the pattern ``xx-name-N`` (e.g. ``us-chicago-1``,
    ``eu-frankfurt-1``).  Rejecting anything else prevents URL-injection
    via the region parameter.
    """
    if not _REGION_PATTERN.match(region):
        raise ValueError(
            f"Invalid OCI region {region!r}. " "Expected format: 'xx-name-N' (e.g. 'us-chicago-1')."
        )
    return region


def _resolve_auth(
    auth: Optional[HttpxOciAuth] = None,
    *,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
) -> HttpxOciAuth:
    """Return an auth instance, creating one from profile if not supplied."""
    if auth is not None:
        return auth

    kwargs: dict[str, Any] = {"profile_name": profile_name}
    if config_file is not None:
        kwargs["config_file"] = config_file

    if auth_type == "user_principal":
        return OciUserPrincipalAuth(**kwargs)
    return OciSessionAuth(**kwargs)


def build_http_client(
    *,
    project_ocid: str,
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
) -> httpx.Client:
    """Build an ``httpx.Client`` with OCI signing and the required project header.

    This is the low-level building block -- use the framework-specific
    builders below for a one-liner experience.

    Parameters
    ----------
    project_ocid:
        The OCI GenAI Project OCID (set as ``OpenAI-Project`` header).
    compartment_id:
        Optional compartment OCID (set as ``opc-compartment-id`` header).
    auth:
        A pre-built ``HttpxOciAuth`` instance.  If ``None``, one is created
        from *profile_name* / *auth_type*.
    profile_name:
        OCI config profile (default ``"DEFAULT"``).  Ignored when *auth*
        is provided.
    auth_type:
        ``"session"`` (default) or ``"user_principal"``.  Ignored when
        *auth* is provided.
    config_file:
        Path to OCI config file.  Defaults to ``~/.oci/config``.
    extra_headers:
        Any additional headers to include on every request.
    """
    resolved_auth = _resolve_auth(
        auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    headers: dict[str, str] = {"OpenAI-Project": project_ocid}
    if compartment_id:
        headers["opc-compartment-id"] = compartment_id
    if extra_headers:
        headers.update(extra_headers)

    return httpx.Client(auth=resolved_auth, headers=headers)


def build_async_http_client(
    *,
    project_ocid: str,
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
) -> httpx.AsyncClient:
    """Build an ``httpx.AsyncClient`` with OCI signing and the required project header.

    Async counterpart of :func:`build_http_client`.
    """
    resolved_auth = _resolve_auth(
        auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    headers: dict[str, str] = {"OpenAI-Project": project_ocid}
    if compartment_id:
        headers["opc-compartment-id"] = compartment_id
    if extra_headers:
        headers.update(extra_headers)

    return httpx.AsyncClient(auth=resolved_auth, headers=headers)


# ---------------------------------------------------------------------------
# OpenAI SDK
# ---------------------------------------------------------------------------


def build_openai_client(
    *,
    project_ocid: str,
    region: str = "us-chicago-1",
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
) -> Any:
    """Return an ``openai.OpenAI`` client wired to OCI Enterprise AI Agents.

    Equivalent to the pattern in ``examples/common.py`` but as a single
    function call.

    Example
    -------
    ::

        from oci_genai_auth import build_openai_client

        client = build_openai_client(
            project_ocid="ocid1.generativeaiproject.oc1...",
            profile_name="DEFAULT",
        )
        resp = client.responses.create(model="openai.gpt-5.2", input="Hello!")
    """
    from openai import OpenAI

    http_client = build_http_client(
        project_ocid=project_ocid,
        compartment_id=compartment_id,
        auth=auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    return OpenAI(
        base_url=_ENDPOINT_TEMPLATE.format(region=_validate_region(region)),
        api_key="not-used",  # Stripped by OciAuth before signing; never sent over the wire.
        project=os.getenv("OCI_GENAI_PROJECT_ID", project_ocid),
        http_client=http_client,
    )


def build_openai_async_client(
    *,
    project_ocid: str,
    region: str = "us-chicago-1",
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
) -> Any:
    """Return an ``openai.AsyncOpenAI`` client wired to OCI Enterprise AI Agents.

    Async counterpart of :func:`build_openai_client`.
    """
    from openai import AsyncOpenAI

    http_client = build_async_http_client(
        project_ocid=project_ocid,
        compartment_id=compartment_id,
        auth=auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    return AsyncOpenAI(
        base_url=_ENDPOINT_TEMPLATE.format(region=_validate_region(region)),
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", project_ocid),
        http_client=http_client,
    )


# ---------------------------------------------------------------------------
# OpenAI Agents SDK
# ---------------------------------------------------------------------------


def configure_openai_agents(
    *,
    project_ocid: str,
    region: str = "us-chicago-1",
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
    disable_tracing: bool = True,
) -> Any:
    """Configure the OpenAI Agents SDK to use OCI Enterprise AI Agents.

    Calls ``set_default_openai_client`` with a properly configured
    ``AsyncOpenAI`` client and optionally disables tracing.  Returns the
    ``AsyncOpenAI`` client for further use.

    Example
    -------
    ::

        from agents import Agent, Runner
        from oci_genai_auth import configure_openai_agents

        configure_openai_agents(
            project_ocid="ocid1.generativeaiproject.oc1...",
        )
        agent = Agent(name="helper", model="openai.gpt-5.2")
        result = await Runner.run(agent, "Write a haiku.")
    """
    try:
        from agents import set_default_openai_client, set_tracing_disabled
    except ImportError as exc:
        raise ImportError(
            "openai-agents is required for OpenAI Agents SDK integration. "
            "Install it with: pip install 'oci-genai-auth[agents]'"
        ) from exc

    async_client = build_openai_async_client(
        project_ocid=project_ocid,
        region=region,
        compartment_id=compartment_id,
        auth=auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    set_default_openai_client(async_client)
    if disable_tracing:
        set_tracing_disabled(True)

    return async_client


# ---------------------------------------------------------------------------
# LangChain / LangGraph
# ---------------------------------------------------------------------------


def build_langchain_chat(
    *,
    model: str,
    project_ocid: str,
    region: str = "us-chicago-1",
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
    use_responses_api: bool = True,
    **kwargs: Any,
) -> Any:
    """Return a ``langchain_openai.ChatOpenAI`` wired to OCI Enterprise AI Agents.

    Also works with **LangGraph** -- LangGraph uses ``ChatOpenAI`` as its
    LLM backend, so the returned object plugs directly into LangGraph nodes.

    Example
    -------
    ::

        from oci_genai_auth import build_langchain_chat

        llm = build_langchain_chat(
            model="openai.gpt-5.2",
            project_ocid="ocid1.generativeaiproject.oc1...",
        )
        response = llm.invoke("Hello!")
    """
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for LangChain/LangGraph integration. "
            "Install it with: pip install 'oci-genai-auth[langchain]'"
        ) from exc

    http_client = build_http_client(
        project_ocid=project_ocid,
        compartment_id=compartment_id,
        auth=auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    return ChatOpenAI(
        model=model,
        api_key="not-used",
        base_url=_ENDPOINT_TEMPLATE.format(region=_validate_region(region)),
        http_client=http_client,
        use_responses_api=use_responses_api,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# PydanticAI
# ---------------------------------------------------------------------------


def build_pydantic_ai_model(
    *,
    model: str,
    project_ocid: str,
    region: str = "us-chicago-1",
    compartment_id: Optional[str] = None,
    auth: Optional[HttpxOciAuth] = None,
    profile_name: str = "DEFAULT",
    auth_type: str = "session",
    config_file: Optional[str] = None,
) -> Any:
    """Return a ``pydantic_ai.models.openai.OpenAIModel`` wired to OCI Enterprise AI Agents.

    Example
    -------
    ::

        from pydantic_ai import Agent
        from oci_genai_auth import build_pydantic_ai_model

        model = build_pydantic_ai_model(
            model="openai.gpt-5.2",
            project_ocid="ocid1.generativeaiproject.oc1...",
        )
        agent = Agent(model)
        result = agent.run_sync("What is 2+2?")
    """
    try:
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider
    except ImportError as exc:
        raise ImportError(
            "pydantic-ai is required for PydanticAI integration. "
            "Install it with: pip install 'oci-genai-auth[pydantic-ai]'"
        ) from exc

    from openai import AsyncOpenAI as _AsyncOpenAI

    async_http_client = build_async_http_client(
        project_ocid=project_ocid,
        compartment_id=compartment_id,
        auth=auth,
        profile_name=profile_name,
        auth_type=auth_type,
        config_file=config_file,
    )

    async_client = _AsyncOpenAI(
        base_url=_ENDPOINT_TEMPLATE.format(region=_validate_region(region)),
        api_key="not-used",
        project=os.getenv("OCI_GENAI_PROJECT_ID", project_ocid),
        http_client=async_http_client,
    )

    provider = OpenAIProvider(openai_client=async_client)
    return OpenAIModel(model, provider=provider)
