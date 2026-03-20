# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates streaming results from the web_search tool."""
from oci_genai_support.openai.oci_openai import OPC_COMPARTMENT_ID_HEADER

from examples.agenthub import common

MODEL="xai.grok-4-1-fast-reasoning"

def main():
    client = common.build_agenthub_client()

    response_stream = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search"}],
        input="What was a positive news story on 2026-03-06?",
        stream=True,
    )

    for event in response_stream:
        print(event)


if __name__ == "__main__":
    main()
