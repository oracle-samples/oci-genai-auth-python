# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates retrieving a response from the Responses API."""

from examples.agenthub.openai import common


def main():
    client = common.build_agenthub_client()

    # Create a response first
    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input="What is 2x2?",
    )
    print("Created response ID:", response.id)

    # Retrieve the response by ID
    retrieved = client.responses.retrieve(response_id=response.id)
    print("Retrieved response:", retrieved.output_text)


if __name__ == "__main__":
    main()
