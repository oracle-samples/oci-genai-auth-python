# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

MODEL = "openai.gpt-4.1"


tools = [
    {
        "type": "mcp",
        "server_label": "deepwiki",
        "require_approval": "never",
        "server_url": "https://mcp.deepwiki.com/mcp",
    },
    {
        "type": "web_search",
    },
]


# parrel_call
response = openai_client.responses.create(
    model=MODEL,
    input="search latest repo related to react, and use deepwiki tell me repo structure",
    tools=tools,
)
print(response.output)
