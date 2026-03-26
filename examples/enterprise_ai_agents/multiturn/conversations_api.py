# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates a multi-turn flow using the Conversations API."""

from examples.enterprise_ai_agents import common

MODEL = "xai.grok-4-1-fast-reasoning"


def main():
    client = common.build_enterprise_ai_agents_client()

    # Create a conversation upfront
    conversation = client.conversations.create(metadata={"topic": "demo"})
    print("Conversation ID:", conversation.id)

    # First turn
    response1 = client.responses.create(
        model=MODEL,
        input="Tell me a joke. Keep it short.",
        conversation=conversation.id,
    )
    print("Response 1:", response1.output_text)

    # Second turn on the same conversation
    response2 = client.responses.create(
        model=MODEL,
        input="Why is it funny?",
        conversation=conversation.id,
    )
    print("Response 2:", response2.output_text)


if __name__ == "__main__":
    main()
