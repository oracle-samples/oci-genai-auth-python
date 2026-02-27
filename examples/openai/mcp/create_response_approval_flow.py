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
        "require_approval": "always",
        "server_url": "https://mcp.deepwiki.com/mcp",
    }
]
response1 = openai_client.responses.create(
    model=MODEL, input="please tell me structure about facebook/react", tools=tools, store=True
)

print(response1.output)

approve_id = response1.output[1].id
id = response1.id

approval_response = {
    "type": "mcp_approval_response",
    "approval_request_id": approve_id,
    "approve": True,
}


response2 = openai_client.responses.create(
    model=MODEL, input=[approval_response], tools=tools, previous_response_id=id
)
print(response2.output)
