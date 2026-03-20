# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates creating a response with storage disabled using the Responses API."""

from examples import common


def main():
    client = common.build_openai_agenthub_client()

    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input="What is 2x2?",
        store=False,
    )
    print(response.output_text)

    # Try to retrieve the response by ID, and it should throw openai.NotFoundError
    retrieved = client.responses.retrieve(response_id=response.id)
    print(f"Response: {retrieved}")


if __name__ == "__main__":
    main()
