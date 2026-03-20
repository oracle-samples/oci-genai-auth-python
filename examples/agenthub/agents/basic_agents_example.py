# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/


"""Demonstrates running an OpenAI Agents workflow against the AgentHub endpoint."""

import asyncio

from agents import Agent, Runner, set_default_openai_client, trace

from examples.agenthub import common

MODEL = "xai.grok-4-1-fast-reasoning"

# Set the OCI OpenAI Client as the default client to use with OpenAI Agents
set_default_openai_client(common.build_agenthub_async_client())


async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=MODEL)
    # https://openai.github.io/openai-agents-python/models/#tracing-client-error-401
    with trace("Trace workflow"):
        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
