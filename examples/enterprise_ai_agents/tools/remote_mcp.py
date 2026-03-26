# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates calling a remote MCP tool."""

from examples.enterprise_ai_agents import common


def main():
    client = common.build_enterprise_ai_agents_client()

    response_stream = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        tools=[
            {
                "type": "mcp",
                "server_label": "dmcp",
                "server_description": "A Dungeons and Dragons MCP server to "
                "assist with dice rolling.",
                "server_url": "https://mcp.deepwiki.com/mcp",
                "require_approval": "never",
            },
        ],
        input="Roll 2d4+1",
        stream=True,
    )

    for event in response_stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)

    print()


if __name__ == "__main__":
    main()
