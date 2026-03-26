# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates parallel function-calling tools with the Responses API."""

from rich import print

from examples.enterprise_ai_agents import common
from examples.fc_tools import fc_tools

MODEL = "xai.grok-4-1-fast-reasoning"


def main():
    openai_client = common.build_enterprise_ai_agents_client()
    # parrel_call
    response = openai_client.responses.create(
        model=MODEL,
        input="what is the weather in seattle and in new York?",
        previous_response_id=None,  # root of the history
        tools=fc_tools,
    )
    print(response.output)

    # no parrel_call

    response = openai_client.responses.create(
        model=MODEL,
        input="what is the weather in seattle and in new York?",
        previous_response_id=None,  # root of the history
        tools=fc_tools,
        parallel_tool_calls=False,
    )
    print(response.output)


if __name__ == "__main__":
    main()
