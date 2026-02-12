# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from typing import Any, Mapping, Optional

import httpx
from openai._base_client import DefaultAsyncHttpxClient, DefaultHttpxClient
from openai._client import AsyncOpenAI, OpenAI, Timeout
from openai._constants import DEFAULT_MAX_RETRIES
from openai._types import NOT_GIVEN, NotGiven

from ..auth import (  # noqa: F401
    HttpxOciAuth,
    OciInstancePrincipalAuth,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)

API_KEY = "<NOTUSED>"
COMPARTMENT_ID_HEADER = "CompartmentId"
OPC_COMPARTMENT_ID_HEADER = "opc-compartment-id"
CONVERSATION_STORE_ID_HEADER = "opc-conversation-store-id"


class OciOpenAI(OpenAI):
    """
    A custom OpenAI client implementation for Oracle Cloud Infrastructure (OCI).

    This class extends the OpenAI client to work with OCI Generative AI service
    endpoints and OpenAI-compatible OCI Data Science Model Deployment endpoints,
    handling authentication and request signing specific to OCI.

    Attributes:
        auth (httpx.Auth): Authentication handler for OCI request signing.
        region (str | None): The OCI service region, e.g., 'us-chicago-1'.
                             Must be provided if service_endpoint and base_url are None
        service_endpoint (str | None): The OCI service endpoint. when service_endpoint
                                       provided, the region will be ignored.
        base_url (str | None): The OCI service full path URL. when base_url provided, the region
                               and service_endpoint will be ignored.
        compartment_id (str | None): OCI compartment OCID for resource isolation, required for
                                     Generative AI Service, Optional for Data Science Service
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Maximum number of retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        region: str = None,
        service_endpoint: str = None,
        base_url: str = None,
        compartment_id: str = None,
        conversation_store_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        base_url = _resolve_base_url(region, service_endpoint, base_url)

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )
        http_client_headers = _build_headers(compartment_id, conversation_store_id)

        super().__init__(
            api_key=API_KEY,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=DefaultHttpxClient(
                auth=auth,
                headers=http_client_headers,
            ),
            **kwargs,
        )


class AsyncOciOpenAI(AsyncOpenAI):
    """
    An async OpenAI-compatible client for Oracle Cloud Infrastructure (OCI).

    Supports OCI Generative AI service endpoints and OpenAI-compatible
    OCI Data Science Model Deployment endpoints with async/await,
    handling OCI-specific authentication and request signing.

    Attributes:
        auth (httpx.Auth): Authentication handler for OCI request signing.
        region (str | None): The OCI service region, e.g., 'us-chicago-1'.
                             Must be provided if service_endpoint and base_url are None
        service_endpoint (str | None): The OCI service endpoint. when service_endpoint
                                       provided, the region will be ignored.
        base_url (str | None): The OCI service full path URL. when base_url provided, the region
                               and service_endpoint will be ignored.
        compartment_id (str | None): OCI compartment OCID for resource isolation, required for
                                     Generative AI Service, Optional for Data Science Service
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Max retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        region: str = None,
        service_endpoint: str = None,
        base_url: str = None,
        compartment_id: Optional[str] = None,
        conversation_store_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        base_url = _resolve_base_url(region, service_endpoint, base_url)

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )
        http_client_headers = _build_headers(compartment_id, conversation_store_id)

        super().__init__(
            api_key=API_KEY,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=DefaultAsyncHttpxClient(
                auth=auth,
                headers=http_client_headers,
            ),
            **kwargs,
        )


def _build_service_endpoint(region: str) -> str:
    return f"https://inference.generativeai.{region}.oci.oraclecloud.com"


def _build_base_url(service_endpoint: str) -> str:
    url = service_endpoint.rstrip(" /")
    return f"{url}/openai/v1"


def _resolve_base_url(region: str = None, service_endpoint: str = None, base_url: str = None):
    # build service endpoint by region when service_endpoint is empty,
    # then build base url from service endpoint
    if not base_url and not service_endpoint and not region:
        raise ValueError("Region or service endpoint or base url must be provided.")
    base_url = (
        base_url
        if base_url
        else _build_base_url(
            service_endpoint if service_endpoint else _build_service_endpoint(region)
        )
    )
    return base_url


def _build_headers(compartment_id: str = None, conversation_store_id: str = None):
    http_client_headers = (
        {
            COMPARTMENT_ID_HEADER: compartment_id,  # for backward compatibility
            OPC_COMPARTMENT_ID_HEADER: compartment_id,
        }
        if compartment_id
        else {}
    )
    if conversation_store_id:
        http_client_headers[CONVERSATION_STORE_ID_HEADER] = conversation_store_id
    return http_client_headers
