# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates a basic chat completion request for the Partner (pass-through) endpoint."""

from rich import print

from examples.partner.openai import common

MODEL = "openai.gpt-4.1"


def main():
    openai_client = common.build_openai_pt_client()

    completion = openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "List three creative uses for a paperclip."},
        ],
        max_tokens=128,
    )

    print(completion.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
