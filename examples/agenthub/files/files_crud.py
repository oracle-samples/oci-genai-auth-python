# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates CRUD operations for files."""

from pathlib import Path

from examples.agenthub import common


def main():
    client = common.build_agenthub_client()
    # List files in the project
    files_list = client.files.list(order="asc")
    for file in files_list.data:
        print(f"ID: {file.id:<45} Status:{file.status:<10} Name:{file.filename}")

    pdf_file_path = Path(__file__).parent / "sample_doc.pdf"

    # Upload a file
    with open(pdf_file_path, "rb") as f:
        file = client.files.create(file=f, purpose="user_data")
        print("Uploaded file:", file)

    # Retrieve file metadata
    retrieved_result = client.files.retrieve(file_id=file.id)
    print("\nRetrieved file:", retrieved_result)
    print("\nWaiting for file to get processed")
    client.files.wait_for_processing(file.id)

    # Delete file
    delete_result = client.files.delete(file_id=file.id)
    print("\nDelete result:", delete_result)


if __name__ == "__main__":
    main()
