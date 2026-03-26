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

from openai import OpenAI

from examples.enterprise_ai_agents.common import PROJECT_OCID


def main():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        project=os.getenv("OCI_GENAI_PROJECT_ID", PROJECT_OCID),
        base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    )
    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input="What is 2x2?",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
