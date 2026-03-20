# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates providing image input via URL to the Responses API."""

from examples.agenthub.openai import common


def main():
    client = common.build_agenthub_client()

    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        store=False,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "What's in this image?",
                    },
                    {
                        "type": "input_image",
                        "image_url": "https://picsum.photos/id/237/200/300",
                    },
                ],
            }
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
