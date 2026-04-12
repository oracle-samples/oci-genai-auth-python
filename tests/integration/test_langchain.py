# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Integration tests for LangChain / LangGraph builder."""

from __future__ import annotations

from tests.conftest import requires_oci


@requires_oci
class TestLangChain:
    def test_build_langchain_chat(
        self,
        oci_project_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        from oci_genai_auth import build_langchain_chat

        llm = build_langchain_chat(
            model=oci_model,
            project_ocid=oci_project_id,
            region=oci_region,
            auth_type=oci_auth_type,
            profile_name=oci_profile,
        )
        resp = llm.invoke("What is 2+2?")
        assert str(resp.content), "Expected non-empty response"
