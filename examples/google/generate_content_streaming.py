# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common

MODEL = "gemini-2.0-flash-001"


def _build_client():
    return common.build_google_client()


def main() -> None:
    client = _build_client()

    stream = client.models.generate_content_stream(
        model=MODEL,
        contents="Stream a short poem about the ocean in 4 lines.",
    )

    for chunk in stream:
        print(chunk)


if __name__ == "__main__":
    main()
