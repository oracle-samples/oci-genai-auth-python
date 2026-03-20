# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates searching vector stores."""

import time

from examples.agenthub.openai import common


def main():
    dp_client = common.build_agenthub_client()
    with open("../files/sample_doc.pdf", "rb") as f:
        # Upload a file using the Files API
        file = dp_client.files.create(
            file=f,
            purpose="user_data",
        )
        print(f"Uploaded file:{file.id}, waiting for it to be processed")
        # dp_client.files.wait_for_processing(file.id)

        cp_client = common.build_agenthub_cp_client()
        # Create a vector store
        vector_store = cp_client.vector_stores.create(
            name="OCI Support FAQ Vector Store",
            description="My vector store for supporting customer queries",
            expires_after={
                "anchor": "last_active_at",
                "days": 30,
            },
        )
        print("Created vector store:", vector_store.id)

        # Wait for vector store resource to be in the "completed" state
        while True:
            vector_store = cp_client.vector_stores.retrieve(vector_store_id=vector_store.id)
            print("Vector store status:", vector_store.status)
            if vector_store.status == "completed":
                break
            else:
                time.sleep(5)

        # Wait a few more seconds after completed state for the vector store to be fully activated
        time.sleep(10)

        # Add a file to a vector store using the Vector Store Files API
        create_result = dp_client.vector_stores.files.create(
            vector_store_id=vector_store.id,
            file_id=file.id,
            attributes={"category": "docfiles"},
        )
        print("Created vector store file:", create_result)

        while True:
            file_status = dp_client.vector_stores.files.retrieve(
                vector_store_id=vector_store.id,
                file_id=file.id,
            )
            print("Vector store file status:", file_status.status)
            if file_status.status == "completed":
                break
            else:
                time.sleep(3)

        # Now the vector store file is indexed, we can search the vector store by a query term
        search_results_page = dp_client.vector_stores.search(
            vector_store_id=vector_store.id,
            query="OCI GenAI Auth",
            max_num_results=10,
        )
        print("\nSearch results page:", search_results_page)

        if search_results_page.data:
            for page_data in search_results_page.data:
                print("\nSearch results page data:", page_data)
        else:
            print("\nNo search results found")


if __name__ == "__main__":
    main()
