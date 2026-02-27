# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common

MODEL = "claude-opus-4-6"


def _build_client():
    return common.build_anthropic_client()


def main() -> None:
    client = _build_client()

    message = client.beta.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": "Summarize the key points from https://www.anthropic.com"
                " in 2-3 sentences.",
            }
        ],
        tools=[
            {
                "type": "web_fetch_20250910",
                "name": "web_fetch",
                "max_uses": 1,
            }
        ],
        betas=["web-fetch-2025-09-10"],
    )

    print(message)


if __name__ == "__main__":
    main()
