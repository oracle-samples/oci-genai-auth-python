# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

MODEL = "openai.gpt-4.1"
tools = [
    {
        "type": "mcp",
        "server_label": "stripe",
        "require_approval": "never",
        "server_url": "https://mcp.stripe.com",
        "authorization": "<test key>",
    }
]
response1 = openai_client.responses.create(
    model=MODEL,
    input="Please use stirpe create account with a and a@g.com",
    tools=tools,
    store=True,
)

print(response1.output)
