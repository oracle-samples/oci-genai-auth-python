# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Async quickstart using Generative AI API Key authentication with Chat Completions."""

import asyncio
import os

from examples import common

MODEL = os.getenv("OCI_GENAI_CHAT_MODEL", "meta.llama-4-scout-17b-16e-instruct")


async def main():
    client = common.build_api_key_async_openai_client()
    try:
        completion = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise assistant.",
                },
                {
                    "role": "user",
                    "content": "How do I output all files in a directory using Python?",
                },
            ],
        )
        print(completion.choices[0].message.content)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
