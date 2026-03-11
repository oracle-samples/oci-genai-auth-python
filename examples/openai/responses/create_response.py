# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

model = "openai.gpt-5"

# First Request
response1 = openai_client.responses.create(
    model=model,
    input="Explain what OKRs are in 2 sentences.",
    previous_response_id=None,  # root of the history
)
print(response1)
