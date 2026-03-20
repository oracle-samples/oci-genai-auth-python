# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates streaming chat completion responses for the Partner (pass-through) endpoint."""

from examples.partner import common

MODEL = "openai.gpt-5.2"


def main():
    openai_client = common.build_openai_client()

    stream = openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant who answers in one paragraph.",
            },
            {
                "role": "user",
                "content": "Explain why the sky is blue as if you were a physics teacher.",
            },
        ],
        stream=True,
    )

    for chunk in stream:
        for choice in chunk.choices:
            delta = choice.delta
            if delta.content:
                print(delta.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
