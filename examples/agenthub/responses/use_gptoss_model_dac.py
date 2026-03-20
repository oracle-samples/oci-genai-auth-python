# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates using a GPT OSS DAC model with the Responses API."""

from examples.agenthub import common


def main():
    client = common.build_agenthub_client()

    response = client.responses.create(
        model="<your-dac-endpoint-ocid-that-hosts-the-gpt-oss-model>",
        input="What is 2x2?",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
