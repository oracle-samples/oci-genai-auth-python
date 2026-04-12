# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Integration tests for OpenAI SDK and OpenAI Agents SDK builders."""

from __future__ import annotations

import asyncio

from tests.conftest import requires_oci


@requires_oci
class TestOpenAISDK:
    def test_build_openai_client(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        from oci_genai_auth import build_openai_client

        client = build_openai_client(
            project_ocid=oci_project_id,
            region=oci_region,
            auth_type=oci_auth_type,
            profile_name=oci_profile,
        )
        resp = client.responses.create(
            model=oci_model,
            input="What is 2+2?",
            store=False,
        )
        assert resp.output_text, "Expected non-empty response"

    def test_build_openai_async_client(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        from oci_genai_auth import build_openai_async_client

        async def _run():
            client = build_openai_async_client(
                project_ocid=oci_project_id,
                region=oci_region,
                auth_type=oci_auth_type,
                profile_name=oci_profile,
            )
            resp = await client.responses.create(
                model=oci_model,
                input="What is 2+2?",
                store=False,
            )
            return resp.output_text

        output = asyncio.run(_run())
        assert output, "Expected non-empty response"


@requires_oci
class TestOpenAIAgentsSDK:
    def test_configure_openai_agents(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        from agents import Agent, Runner

        from oci_genai_auth import configure_openai_agents

        configure_openai_agents(
            project_ocid=oci_project_id,
            region=oci_region,
            auth_type=oci_auth_type,
            profile_name=oci_profile,
            disable_tracing=True,
        )

        async def _run():
            agent = Agent(
                name="test",
                instructions="You are a helpful assistant.",
                model=oci_model,
            )
            result = await Runner.run(agent, "What is 2+2?")
            return result.final_output

        output = asyncio.run(_run())
        assert output, "Expected non-empty response"
