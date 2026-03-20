# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates providing image input via base64 to the Responses API."""

import base64
from pathlib import Path

from examples.agenthub.openai import common


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main():
    client = common.build_agenthub_client()

    # assuming the file "Cat.jpg" is in the same directory as this script
    image_file_path = Path(__file__).parent / "Cat.jpg"
    base64_image = encode_image(image_file_path)

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
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high",
                    },
                ],
            }
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
