# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

conversation = openai_client.conversations.create(
    metadata={"topic": "demo"}, items=[{"type": "message", "role": "user", "content": "Hello!"}]
)
print(conversation)
