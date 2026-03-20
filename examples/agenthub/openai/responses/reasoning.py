# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates a reasoning-style Responses API request."""

from examples import common


def main():
    client = common.build_openai_agenthub_client()

    prompt = """
    Write a bash script that takes a matrix represented as a string with
    format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
    """

    response = client.responses.create(
        model="openai.gpt-oss-120b",
        input=prompt,
        reasoning={"effort": "medium", "summary": "detailed"},
        stream=True,
    )
    for event in response:
        if event.type == "response.reasoning_summary_part.added":
            print("Thinking...")
        if event.type == "response.reasoning_summary_text.delta":
            print(event.delta, end="", flush=True)
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
