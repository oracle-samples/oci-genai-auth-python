# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from .auth import (
    HttpxOciAuth,
    OciAuthRefreshError,
    OciInstancePrincipalAuth,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)
from .frameworks import (
    build_async_http_client,
    build_http_client,
    build_langchain_chat,
    build_openai_async_client,
    build_openai_client,
    build_pydantic_ai_model,
    configure_openai_agents,
)

__all__ = [
    # Auth
    "HttpxOciAuth",
    "OciAuthRefreshError",
    "OciInstancePrincipalAuth",
    "OciResourcePrincipalAuth",
    "OciSessionAuth",
    "OciUserPrincipalAuth",
    # Framework helpers
    "build_async_http_client",
    "build_http_client",
    "build_langchain_chat",
    "build_openai_async_client",
    "build_openai_client",
    "build_pydantic_ai_model",
    "configure_openai_agents",
]
