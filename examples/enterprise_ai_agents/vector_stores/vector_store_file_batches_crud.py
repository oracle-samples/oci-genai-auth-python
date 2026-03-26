# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates CRUD operations for vector store file batches."""

from examples.enterprise_ai_agents import common

VECTOR_STORE_ID = "<<VECTOR_STORE_OCID>>"


def main():
    client = common.build_enterprise_ai_agents_client()
    with open("../files/sample_doc.pdf", "rb") as f1, open("../files/sample_doc.pdf", "rb") as f2:
        file_1 = client.files.create(
            file=f1,
            purpose="user_data",
        )
        file_2 = client.files.create(
            file=f2,
            purpose="user_data",
        )
        # Create a batch with file IDs and shared attributes
        batch_result = client.vector_stores.file_batches.create(
            vector_store_id=VECTOR_STORE_ID,
            file_ids=[file_1.id, file_2.id],
            attributes={"category": "history"},
        )
        print("Created batch:", batch_result)

        # Retrieve batch status
        retrieve_result = client.vector_stores.file_batches.retrieve(
            vector_store_id=VECTOR_STORE_ID,
            batch_id=batch_result.id,
        )
        print("\nBatch status:", retrieve_result)

        # List files in a batch
        list_result = client.vector_stores.file_batches.list_files(
            vector_store_id=VECTOR_STORE_ID,
            batch_id=batch_result.id,
        )
        print("\nBatch files:", list_result)


if __name__ == "__main__":
    main()
