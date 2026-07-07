# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using Generative AI API Key authentication with Chat Completions.

This example uses the native OpenAI client with an OCI Generative AI API Key.
No oci-genai-auth package is needed for API Key auth - just the official OpenAI SDK.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. Create a Generative AI API Key on OCI Console
  3. Export OPENAI_API_KEY
  4. Run this script
"""

import os

from examples import common

MODEL = os.getenv("OCI_GENAI_CHAT_MODEL", "meta.llama-4-scout-17b-16e-instruct")


def main():
    client = common.build_api_key_openai_client()

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant.",
            },
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
