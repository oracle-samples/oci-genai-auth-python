# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using Generative AI API Key authentication.

This example uses the native OpenAI client with OCI Generative AI API Key.
No oci-genai-auth package needed for API Key auth - just the official OpenAI SDK.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. Create a Generative AI API Key on OCI Console
  3. Run this script
"""

import os

from examples import common

MODEL = os.getenv("OCI_GENAI_RESPONSES_MODEL", "xai.grok-4-1-fast-reasoning")
PROMPT = "What is 2x2?"


def main():
    client = common.build_api_key_openai_client()
    response = client.responses.create(
        model=MODEL,
        input=PROMPT,
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
