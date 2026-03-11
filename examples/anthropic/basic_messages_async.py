# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import asyncio

from examples import common

MODEL = "claude-opus-4-6"


async def main() -> None:
    client = common.build_anthropic_async_client()

    message = await client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ],
    )
    print(message.model_dump_json(indent=2))
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
