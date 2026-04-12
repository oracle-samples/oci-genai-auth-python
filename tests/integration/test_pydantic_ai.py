# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Integration tests for PydanticAI builder."""

from __future__ import annotations

from tests.conftest import requires_oci


@requires_oci
class TestPydanticAI:
    def test_build_pydantic_ai_model(
        self,
        oci_project_id,
        oci_compartment_id,
        oci_region,
        oci_profile,
        oci_auth_type,
        oci_model,
    ):
        from pydantic_ai import Agent

        from oci_genai_auth import build_pydantic_ai_model

        model = build_pydantic_ai_model(
            model=oci_model,
            project_ocid=oci_project_id,
            compartment_id=oci_compartment_id,
            region=oci_region,
            auth_type=oci_auth_type,
            profile_name=oci_profile,
        )
        agent = Agent(model)
        result = agent.run_sync("What is 2+2?")
        assert str(result.output), "Expected non-empty response"
