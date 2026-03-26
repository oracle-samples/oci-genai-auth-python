# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates providing file input by URL to the Responses API."""

from examples.enterprise_ai_agents import common


def main():
    client = common.build_enterprise_ai_agents_client()

    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        store=False,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Analyze the letter and provide a summary of the key points.",
                    },
                    {
                        "type": "input_file",
                        "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                    },
                ],
            }
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
