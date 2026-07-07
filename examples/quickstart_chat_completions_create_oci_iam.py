# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using OCI IAM authentication with Chat Completions.

This example uses oci-genai-auth with the OpenAI SDK for OCI Enterprise AI Agents.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. pip install oci-genai-auth
  3. Run this script
"""

import os

from examples import common

MODEL = os.getenv("OCI_GENAI_CHAT_MODEL", "meta.llama-4-scout-17b-16e-instruct")


def main():
    client = common.build_oci_iam_openai_client(include_compartment_headers=True)

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
