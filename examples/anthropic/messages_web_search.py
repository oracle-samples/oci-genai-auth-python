# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common

MODEL = "claude-opus-4-6"


def _build_client():
    return common.build_anthropic_client()


def main() -> None:
    client = _build_client()

    message = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": "Find one recent headline about quantum computing and "
                "summarize it in one sentence.",
            }
        ],
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 2,
            }
        ],
    )

    print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
