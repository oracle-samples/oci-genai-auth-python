# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples import common

MODEL = "claude-opus-4-6"


def _build_client():
    return common.build_anthropic_client()


def main() -> None:
    client = _build_client()

    with client.messages.stream(
        model=MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn.",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print()


if __name__ == "__main__":
    main()
