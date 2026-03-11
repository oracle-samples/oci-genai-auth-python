# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common

MODEL = "claude-opus-4-6"
FILE_PATH = ""


def _build_client():
    return common.build_anthropic_client()


def main() -> None:
    if not FILE_PATH:
        raise ValueError(
            "Set large FILE_PATH to the document you want to summarize (this will test compaction)."
        )

    client = _build_client()
    with open(FILE_PATH) as f:
        data = f.read()
        print(f"Number of tokens {len(data)/5.0}")

        message = client.beta.messages.create(
            model=MODEL,
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
                    "content": "The above is the research paper, give me 10 main learnings "
                    "from there. Keep it succint.",
                },
            ],
        )

        print(message.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
