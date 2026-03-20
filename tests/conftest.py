# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _disable_openai_agents_tracing():
    # Prevent OpenAI Agents tracing from emitting external HTTP requests during tests.
    os.environ.setdefault("OPENAI_AGENTS_DISABLE_TRACING", "true")
    try:
        from agents.tracing import set_tracing_disabled
    except (ImportError, ModuleNotFoundError):
        yield
        return
    set_tracing_disabled(True)
    yield
