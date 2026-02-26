# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples.anthropic.common import build_client, get_model


def main() -> None:
    client = build_client()
    data = open("/Users/vasheno/Downloads/sample.txt").read()
    print(f"Number of tokens {len(data)/5.0}")

    message = client.beta.messages.create(
        model=get_model("claude-opus-4-6"),
        max_tokens=400,
        betas=["compact-2026-01-12"],
        context_management={
            "edits": [
                {
                    "type": "compact_20260112",
                    "trigger": {"type": "input_tokens", "value": 50000},
                }
            ]
        },
        messages=[
            {
                "role": "user",
                "content": f"{data}",
            },
            {
                "role": "user",
                "content": "The above is the research paper, give me 10 main learnings from there. Keep it succint.",
            }
        ],
    )

    print(message)


if __name__ == "__main__":
    main()
