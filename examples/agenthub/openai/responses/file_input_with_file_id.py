# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates providing file input by file ID to the Responses API."""

from examples import common


def main():
    client = common.build_openai_agenthub_client()

    # Upload a file first
    with open("../files/sample_doc.pdf", "rb") as f:
        file = client.files.create(
            file=f,
            purpose="user_data",
        )

    # Use the file in a response
    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file.id,
                    },
                    {
                        "type": "input_text",
                        "text": "What's discussed in the file?",
                    },
                ],
            }
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
