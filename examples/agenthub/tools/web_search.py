# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates the web_search tool in AgentHub."""

from examples.agenthub import common

MODEL="openai.gpt-5.2"

def main():
    client = common.build_agenthub_client()

    response = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search"}],
        input="What was a positive news story on 2025-11-14?",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
