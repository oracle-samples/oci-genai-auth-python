# oci-genai-auth

[![PyPI - Version](https://img.shields.io/pypi/v/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)

The **OCI GenAI Auth** Python library provides OCI request-signing helpers for the OpenAI-compatible REST APIs hosted by OCI Generative AI. Partner/Passthrough endpoints do not store conversation history on OCI servers, while AgentHub (non-passthrough) stores data on OCI-managed servers.

## Table of Contents

- [Before you start](#before-you-start)
- [Using OCI IAM Auth](#using-oci-iam-auth)
- [Using API Key Auth](#using-api-key-auth)
- [Using AgentHub APIs (non-passthrough)](#using-agenthub-apis-non-passthrough)
- [Using Partner APIs (passthrough)](#using-partner-apis-passthrough)
- [Running the Examples](#running-the-examples)

## Before you start

**Important!**

Note that this package, as well as API keys package described below, only supports OpenAI, xAi Grok and Meta LLama models on OCI Generative AI.

Before you start using this package, determine if this is the right option for you.

If you are looking for a seamless way to port your code from an OpenAI compatible endpoint to OCI Generative AI endpoint, and you are currently using OpenAI-style API keys, you might want to use [OCI Generative AI API Keys](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm) instead.

With OCI Generative AI API Keys, use the native `openai` SDK like before. Just update the `base_url`, create API keys in your OCI console, insure the policy granting the key access to generative AI services is present and you are good to go.

- Create an API key in Console: **Generative AI** -> **API Keys**
- Create a security policy: **Identity & Security** -> **Policies**

To authorize a specific API Key
```
allow any-user to use generative-ai-family in compartment <compartment-name> where ALL { request.principal.type='generativeaiapikey', request.principal.id='ocid1.generativeaiapikey.oc1.us-chicago-1....' }
```

To authorize any API Key
```
allow any-user to use generative-ai-family in compartment <compartment-name> where ALL { request.principal.type='generativeaiapikey' }
```

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

Use OCI Generative AI API Keys if you want a direct API-key workflow with the OpenAI SDK.

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
