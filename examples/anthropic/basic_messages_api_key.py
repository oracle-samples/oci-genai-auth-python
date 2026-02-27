# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/


from anthropic import Anthropic

MODEL = "claude-opus-4-6"


def main() -> None:
    client = Anthropic(
        api_key="<<API_KEY_HERE>>",
        base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/anthropic",
    )

    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ],
    )
    print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
