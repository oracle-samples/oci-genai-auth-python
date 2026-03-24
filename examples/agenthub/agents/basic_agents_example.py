# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/


"""Demonstrates using OpenAI Agents SDK against the AgentHub endpoint."""

import asyncio
from agents import Agent, Runner, set_default_openai_client, set_tracing_disabled
from examples.agenthub import common

set_default_openai_client(common.build_agenthub_async_client())
set_tracing_disabled(True)

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="xai.grok-4-1-fast-reasoning")
    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
