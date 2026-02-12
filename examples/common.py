# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from oci_genai_auth import OciOpenAI, OciSessionAuth

COMPARTMENT_ID = ""
CONVERSATION_STORE_ID = ""
OVERRIDE_URL = ""
PROFILE_NAME = "oc1"
REGION = ""


oci_openai_client = OciOpenAI(
    auth=OciSessionAuth(profile_name=PROFILE_NAME),
    compartment_id=COMPARTMENT_ID,
    region=REGION,
    service_endpoint=OVERRIDE_URL,
    conversation_store_id=CONVERSATION_STORE_ID,
)
