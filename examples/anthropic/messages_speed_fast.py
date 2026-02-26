# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples.anthropic.common import build_client, get_model


def main() -> None:
    client = build_client()

    message = client.beta.messages.create(
        model=get_model("claude-opus-4-6"),
        max_tokens=200,
        betas=["fast-mode-2026-02-01"],
        speed="fast",
        messages=[
            {
                "role": "user",
                "content": "List five practical tips for better meeting notes.",
            }
        ],
    )

    print(message)


if __name__ == "__main__":
    main()
