# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import base64
from pathlib import Path

from examples import common

MODEL = "claude-opus-4-6"
IMAGE_PATH = Path(__file__).resolve().parents[1] / "oci_openai" / "responses" / "Cat.jpg"


def main() -> None:
    client = common.build_anthropic_client()

    image_data = base64.b64encode(IMAGE_PATH.read_bytes()).decode("utf-8")

    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": "What's in this image?"},
                ],
            }
        ],
    )
    print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
