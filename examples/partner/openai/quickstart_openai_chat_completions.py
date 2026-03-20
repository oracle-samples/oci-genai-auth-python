# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates a simple openai chat completions example."""

import logging

from examples.partner import common

logging.basicConfig(level=logging.DEBUG)

MODEL="openai.gpt-5.2"

def main():
    client = common.build_openai_client()

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.model_dump_json())

    # Process the stream
    print("=" * 80)
    print("Process in streaming mode")
    streaming = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
        stream=True,
    )
    for chunk in streaming:
        print(chunk)


if __name__ == "__main__":
    main()
