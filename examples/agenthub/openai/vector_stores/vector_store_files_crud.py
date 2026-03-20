# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates CRUD operations for vector store files."""

from examples.agenthub.openai import common

VECTOR_STORE_ID = "<<VECTOR_STORE_OCID>>"


def main():
    client = common.build_agenthub_client()
    # Create the file
    with open("../files/sample_doc.pdf", "rb") as f:
        file = client.files.create(
            file=f,
            purpose="user_data",
        )
        print(f"Created a File: {file.id}, now waiting for it to get processed")
        client.files.wait_for_processing(file.id)

        # Add a file to a vector store
        create_result = client.vector_stores.files.create(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file.id,
            attributes={"category": "history"},
        )
        print("\nCreated vector store file:", create_result)

        # List vector store files
        list_result = client.vector_stores.files.list(
            vector_store_id=VECTOR_STORE_ID,
        )
        print("\nFiles:", list_result)

        # Retrieve vector store file
        retrieve_result = client.vector_stores.files.retrieve(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file.id,
        )
        print("\nRetrieved:", retrieve_result)

        # Update vector store file attributes
        update_result = client.vector_stores.files.update(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file.id,
            attributes={"category": "history", "period": "medieval"},
        )
        print("\nUpdated:", update_result)

        # Delete vector store file (removes parsed content, not the original file)
        delete_result = client.vector_stores.files.delete(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file.id,
        )
        print("\nDeleted:", delete_result)


if __name__ == "__main__":
    main()
