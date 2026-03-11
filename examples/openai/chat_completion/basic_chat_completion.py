# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

MODEL = "openai.gpt-4.1"

completion = openai_client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "List three creative uses for a paperclip."},
    ],
    max_tokens=128,
)

print(completion.model_dump_json(indent=2))
