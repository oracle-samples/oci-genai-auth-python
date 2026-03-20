# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates an approval flow for remote MCP tools."""

from examples.agenthub.openai import common


def main():
    client = common.build_agenthub_client()

    # First API request - Ask the model to call the MCP server,
    # and requires your approval to execute the tool call
    response1 = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        tools=[
            {
                "type": "mcp",
                "server_label": "deepwiki",
                "server_url": "https://mcp.deepwiki.com/mcp",
                "require_approval": "always",
            },
        ],
        input="please tell me structure about facebook/react",
    )
    print(response1.output)

    # Find the MCP approval request in the response
    approval_request = next(
        (item for item in response1.output if item.type == "mcp_approval_request"), None
    )
    if not approval_request:
        raise ValueError("No MCP approval request found in response")

    # Build your MCP approval response
    approval_response = {
        "type": "mcp_approval_response",
        "approval_request_id": approval_request.id,
        "approve": True,
    }

    # Second APIrequest - Send the MCP approval response back to the model
    response2 = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input=[approval_response],
        tools=[
            {
                "type": "mcp",
                "server_label": "deepwiki",  # this must match the server_label
                "server_url": "https://mcp.deepwiki.com/mcp",
                "require_approval": "always",
            }
        ],
        previous_response_id=response1.id,
    )
    print(response2.output)


if __name__ == "__main__":
    main()
