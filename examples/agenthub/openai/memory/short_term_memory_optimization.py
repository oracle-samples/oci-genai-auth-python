# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates short-term memory optimization in AgentHub."""

from examples.agenthub.openai import common

MODEL = "xai.grok-4-1-fast-reasoning"


def main():
    client = common.build_agenthub_client()
    # Create a conversation with STMO enabled
    conversation = client.conversations.create(
        metadata={"topic": "demo", "short_term_memory_optimization": "True"},
        items=[{"type": "message", "role": "user", "content": "Hello!"}],
    )

    # Multiple turns - STMO will auto-condense the history
    response = client.responses.create(
        model=MODEL,
        input="I like Fish.",
        conversation=conversation.id,
    )
    print("Turn 1:", response.output_text)

    response = client.responses.create(
        model=MODEL,
        input="I like Beef.",
        conversation=conversation.id,
    )
    print("Turn 2:", response.output_text)

    response = client.responses.create(
        model=MODEL,
        input="I like ice-cream.",
        conversation=conversation.id,
    )
    print("Turn 3:", response.output_text)

    response = client.responses.create(
        model=MODEL,
        input="I like coffee.",
        conversation=conversation.id,
    )
    print("Turn 4:", response.output_text)

    # The STMO summary will be generated automatically


if __name__ == "__main__":
    main()
