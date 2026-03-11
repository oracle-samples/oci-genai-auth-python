# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common


def _build_client():
    return common.build_anthropic_client()


MODEL = "claude-opus-4-6"


def main() -> None:
    client = _build_client()

    message = client.beta.messages.create(
        model=MODEL,
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

    print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
