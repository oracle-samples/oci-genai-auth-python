# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

# mypy: ignore-errors

# OpenAI Agents SDK imports
import asyncio

from agents import Agent, Runner, set_default_openai_client, trace

from examples import common

MODEL = "openai.gpt-4o"


def get_oci_openai_client():
    return common.build_openai_async_client()


# Set the OCI OpenAI Client as the default client to use with OpenAI Agents
set_default_openai_client(get_oci_openai_client())


async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=MODEL)
    # https://openai.github.io/openai-agents-python/models/#tracing-client-error-401
    with trace("Trace workflow"):
        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
