# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from google import genai

MODEL = "google.gemini-2.5-flash"


def main() -> None:
    client = genai.Client(
        api_key="<<API_KEY_HERE>>",
        http_options={
            "base_url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/google"
        },
    )

    response = client.models.generate_content(
        model=MODEL,
        contents="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
