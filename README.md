# oci-genai-auth

[![PyPI - Version](https://img.shields.io/pypi/v/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)

The **OCI GenAI Auth** Python library provides OCI request-signing helpers for the OpenAI-compatible REST APIs hosted by OCI Generative AI. Partner/Passthrough endpoints do not store conversation history on OCI servers, while AgentHub (non-passthrough) stores data on OCI-managed servers.

## Table of Contents

- [Using OCI IAM Auth](#using-oci-iam-auth)
- [Using API Key Auth](#using-api-key-auth)
- [Using AgentHub APIs (non-passthrough)](#using-agenthub-apis-non-passthrough)
- [Using Partner APIs (passthrough)](#using-partner-apis-passthrough)
- [Running the Examples](#running-the-examples)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Using OCI IAM Auth

Use OCI IAM auth when you want to sign requests with your OCI profile (session/user/resource/instance principal) instead of API keys.

```python
import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)
```

## Using API Key Auth

Use OCI Generative AI API Keys if you want a direct API-key workflow with the OpenAI SDK. In-order to create the OCI Generative AI API Keys, follow [this guide](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

## Using AgentHub APIs (non-passthrough)

AgentHub runs in non-pass-through mode and provides a unified interface for interacting with models and agentic capabilities.
It is compatible with OpenAI's Responses API and the Open Responses Spec, enabling developers/users to: build agents with OpenAI SDK.
Only the project OCID is required.

```python
import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    project="ocid1.generativeaiproject.oc1.us-chicago-1.aaaaaaaaexample",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)
```

## Using Partner APIs (passthrough)

Partner endpoints run in pass-through mode and require the compartment OCID header.

```python
import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/v1",
    api_key="not-used",
    default_headers={
        "opc-compartment-id": "ocid1.compartment.oc1..aaaaaaaaexample",
    },
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)
```


## Running the Examples

1. Update `examples/agenthub/openai/common.py` and/or `examples/partner/openai/common.py` with your `COMPARTMENT_ID`, `PROJECT_OCID`, and set the correct `REGION`.
2. Set the `OPENAI_API_KEY` environment variable when an example uses API key authentication.
3. Install optional dev dependencies: `pip install -e '.[dev]'`.

Run an example either by calling its `main()` method or from the command line.

## Contributing

*If your project has specific contribution requirements, update the CONTRIBUTING.md file to ensure those requirements are clearly explained*

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License
Copyright (c) 2026 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at https://oss.oracle.com/licenses/upl/.