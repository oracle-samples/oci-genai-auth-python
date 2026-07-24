# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Generate content asynchronously with OCI IAM authentication."""

import asyncio

from examples import common

MODEL = "google.gemini-2.5-flash"


async def main() -> None:
    client, http_client = common.build_oci_iam_async_google_client()
    try:
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents="Write a one-sentence bedtime story about a unicorn.",
        )
        print(response.text)
    finally:
        await http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
