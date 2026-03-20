# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates CRUD operations for conversations in AgentHub."""

from examples.agenthub import common


def main():
    client = common.build_agenthub_client()

    # Create a conversation
    conversation = client.conversations.create(
        items=[
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello!"}],
            }
        ],
        metadata={"topic": "demo"},
    )
    print("\nCreated conversation:", conversation)

    # Retrieve the conversation
    conversation = client.conversations.retrieve(
        conversation_id=conversation.id,
    )
    print("\nRetrieved conversation:", conversation)

    # Update the conversation with new metadata
    conversation = client.conversations.update(
        conversation_id=conversation.id,
        metadata={"topic": "demo2"},
    )
    print("\nUpdated conversation:", conversation)

    # Delete the conversation
    client.conversations.delete(
        conversation_id=conversation.id,
    )
    print("\nDeleted conversation:", conversation)


if __name__ == "__main__":
    main()
