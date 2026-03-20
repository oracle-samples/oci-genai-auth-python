# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates structured output with the Responses API."""

from pydantic import BaseModel

from examples.agenthub.openai import common


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def main():
    client = common.build_agenthub_client()

    response = client.responses.parse(
        model="xai.grok-4-1-fast-reasoning",
        input=[
            {
                "role": "system",
                "content": "Extract the event information.",
            },
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            },
        ],
        store=False,
        text_format=CalendarEvent,
    )

    event = response.output_parsed
    print(event)


if __name__ == "__main__":
    main()
