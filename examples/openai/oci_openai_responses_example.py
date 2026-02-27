# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

# mypy: ignore-errors
from examples import common

MODEL = "openai.gpt-4o"

PROMPT = "Tell me a three sentence bedtime story about a unicorn."


def get_oci_openai_client():
    return common.build_openai_client()


def main():
    client = get_oci_openai_client()
    response = client.responses.create(model=MODEL, input=PROMPT)
    print(response.output[0].content[0].text)


if __name__ == "__main__":
    main()
