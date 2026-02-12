# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from .auth import (
    HttpxOciAuth,
    OciInstancePrincipalAuth,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)

__all__ = [
    "HttpxOciAuth",
    "OciSessionAuth",
    "OciResourcePrincipalAuth",
    "OciInstancePrincipalAuth",
    "OciUserPrincipalAuth",
]

_OPENAI_EXPORTS = {"OciOpenAI", "AsyncOciOpenAI"}
_openai_import_error: Exception | None = None
_ANTHROPIC_EXPORTS = {"OciAnthropic", "AsyncOciAnthropic"}
_anthropic_import_error: Exception | None = None

try:
    from .openai import AsyncOciOpenAI, OciOpenAI

    __all__.extend(["OciOpenAI", "AsyncOciOpenAI"])
except Exception as exc:  # pragma: no cover - only triggers when openai extra is missing
    _openai_import_error = exc

try:
    from .anthropic import AsyncOciAnthropic, OciAnthropic

    __all__.extend(["OciAnthropic", "AsyncOciAnthropic"])
except Exception as exc:  # pragma: no cover - only triggers when anthropic extra is missing
    _anthropic_import_error = exc


def __getattr__(name: str):
    if name in _OPENAI_EXPORTS:
        raise ImportError(
            "OpenAI support requires the optional dependency. "
            "Install with: pip install \"oci-genai-auth[openai]\""
        ) from _openai_import_error
    if name in _ANTHROPIC_EXPORTS:
        raise ImportError(
            "Anthropic support requires the optional dependency. "
            "Install with: pip install \"oci-genai-auth[anthropic]\""
        ) from _anthropic_import_error
    raise AttributeError(name)
