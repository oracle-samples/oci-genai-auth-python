# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples import common

MODEL = "gemini-3.1-flash-image-preview"


def main() -> None:
    client = common.build_google_client()

    response = client.models.generate_content(
        model=MODEL,
        contents=["A poster of a mythical dragon in a neon city."],
    )
    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")


if __name__ == "__main__":
    main()
