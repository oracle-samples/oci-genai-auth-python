# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates streaming Responses API output and handling text deltas."""

from examples import common


def main():
    client = common.build_openai_agenthub_client()

    response_stream = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input="What are the shapes of OCI GPUs?",
        stream=True,
    )

    for event in response_stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)

    print()


if __name__ == "__main__":
    main()
