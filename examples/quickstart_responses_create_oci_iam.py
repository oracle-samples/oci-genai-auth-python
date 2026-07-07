# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using OCI IAM authentication.

This example uses oci-genai-auth with the OpenAI SDK for OCI Enterprise AI Agents.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. pip install oci-genai-auth
  3. Run this script
"""

import os

from examples import common

MODEL = os.getenv("OCI_GENAI_RESPONSES_MODEL", "xai.grok-4-1-fast-reasoning")
PROMPT = "What is 2x2?"


def main():
    client = common.build_oci_iam_openai_client()

    response = client.responses.create(
        model=MODEL,
        input=PROMPT,
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
