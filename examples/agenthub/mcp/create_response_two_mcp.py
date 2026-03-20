# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates a two-step MCP response flow."""

from rich import print

from examples.agenthub import common

MODEL = "xai.grok-4-1-fast-reasoning"


def main():
    openai_client = common.build_agenthub_client()

    tools = [
        {
            "type": "mcp",
            "server_label": "stripe",
            "require_approval": "never",
            "server_url": "https://mcp.stripe.com",
            "authorization": "<test key>",
        },
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "require_approval": "never",
            "server_url": "https://mcp.deepwiki.com/mcp",
        },
    ]
    response1 = openai_client.responses.create(
        model=MODEL,
        input="Please use stirpe create account with a and a@g.com and "
        "use deepwiki understand facebook/react",
        tools=tools,
        store=True,
    )

    print(response1.output)


if __name__ == "__main__":
    main()
