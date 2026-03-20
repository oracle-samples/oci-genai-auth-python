# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates the file_search tool in AgentHub."""

from examples.agenthub import common

VECTOR_STORE_ID = "<<VECTORE_STORE_ID>>"


def main():
    client = common.build_agenthub_client()

    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input="What are shapes of OCI GPU?",
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
            }
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
