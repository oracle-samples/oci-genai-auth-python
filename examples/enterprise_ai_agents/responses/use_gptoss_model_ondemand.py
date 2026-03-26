# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates using a GPT OSS on-demand model with the Responses API."""

from examples.enterprise_ai_agents import common

MODEL="openai.gpt-oss-120b"

def main():
    client = common.build_enterprise_ai_agents_client()

    response = client.responses.create(
        model=MODEL,
        input="What is 2x2?",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
