# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Vector Stores API examples - create, list, retrieve, update, search, and delete."""

from examples import common


def main():
    cp_client = common.build_openai_agenthub_cp_client()
    # Create a vector store
    vector_store = cp_client.vector_stores.create(
        name="OCI Support FAQ Vector Store",
        description="My vector store for supporting customer queries",
        expires_after={
            "anchor": "last_active_at",
            "days": 30,
        },
        metadata={
            "topic": "oci",
        },
    )
    print("Created vector store:", vector_store.id)

    # List vector stores
    list_result = cp_client.vector_stores.list(limit=20, order="desc")
    print("\nVector stores:", list_result)

    # Retrieve vector store
    retrieve_result = cp_client.vector_stores.retrieve(
        vector_store_id=vector_store.id,
    )
    print("\nRetrieved:", retrieve_result)

    # Update vector store
    update_result = cp_client.vector_stores.update(
        vector_store_id=vector_store.id,
        name="Updated Demo Vector Store",
        metadata={"category": "history", "period": "medieval"},
    )
    print("\nUpdated:", update_result)

    # Delete vector store
    delete_result = cp_client.vector_stores.delete(
        vector_store_id=vector_store.id,
    )
    print("\nDeleted:", delete_result)


if __name__ == "__main__":
    main()
