# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples.anthropic.common import build_client, get_model


def main() -> None:
    client = build_client()

    message = client.messages.create(
        model=get_model("claude-opus-4-6"),
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": "Find one recent headline about quantum computing and summarize it in one sentence.",
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

    print(message)


if __name__ == "__main__":
    main()
