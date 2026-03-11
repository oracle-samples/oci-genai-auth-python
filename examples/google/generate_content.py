# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples import common

MODEL = "google.gemini-2.5-flash"


def main() -> None:
    client = common.build_google_client()

    response = client.models.generate_content(
        model=MODEL,
        contents="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
