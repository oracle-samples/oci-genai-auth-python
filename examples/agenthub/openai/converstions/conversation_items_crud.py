# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates CRUD operations for conversation items in AgentHub."""

from examples import common


def main():
    # Create an empty conversation
    cp_client = common.build_openai_agenthub_client()
    conversation = cp_client.conversations.create()
    print("\nCreated conversation:", conversation)

    # Create items in the conversation
    cp_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "What's your name?"}],
            },
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "What's your favorite color?"}],
            },
        ],
    )

    # List the items in the conversation after creating items
    items = cp_client.conversations.items.list(
        conversation_id=conversation.id,
    )
    print("\nConversation items after creating items:", items.data)

    # Delete an item from the conversation
    cp_client.conversations.items.delete(
        conversation_id=conversation.id,
        item_id=items.data[0].id,
    )

    # List the items in the conversation after deleting an item
    items = cp_client.conversations.items.list(
        conversation_id=conversation.id,
    )
    print("\nConversation items after creating items:", items.data)


if __name__ == "__main__":
    main()
