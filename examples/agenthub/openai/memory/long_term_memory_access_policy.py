# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates long-term memory access policies in AgentHub."""

import time

from examples.agenthub.openai import common

MODEL = "openai.gpt-5.1"


def main():
    client = common.build_agenthub_client()
    # First conversation - store only (no recall)
    conversation1 = client.conversations.create(
        metadata={
            "memory_subject_id": "user_123456",
            "memory_access_policy": "store_only",
        },
    )

    response = client.responses.create(
        model=MODEL,
        input="I like Fish. I don't like Shrimp.",
        conversation=conversation1.id,
    )
    print("Response 1:", response.output_text)

    # Delay for long-term memory processing
    print("Waiting for long-term memory processing...")
    time.sleep(20)

    # Second conversation - recall only (no new storage)
    conversation2 = client.conversations.create(
        metadata={
            "memory_subject_id": "user_123456",
            "memory_access_policy": "recall_only",
        },
    )

    response = client.responses.create(
        model=MODEL,
        input="What food do I like?",
        conversation=conversation2.id,
    )
    print("Response 2:", response.output_text)


if __name__ == "__main__":
    main()
