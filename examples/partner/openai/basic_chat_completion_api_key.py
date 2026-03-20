# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates the Basic chat completion api key example."""

import os

from openai import OpenAI

MODEL = "openai.gpt-5.2"


def main() -> None:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant who answers in one paragraph.",
            },
            {
                "role": "user",
                "content": "Explain why the sky is blue as if you were a physics teacher.",
            },
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
