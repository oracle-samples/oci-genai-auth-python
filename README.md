# oci-genai-auth

[![PyPI - Version](https://img.shields.io/pypi/v/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)

The **OCI GenAI Auth** Python library provides secure and convenient access to the OpenAI-compatible REST API hosted by **OCI Generative AI Service** and **OCI Data Science Model Deployment** Service.

---

## Table of Contents

- [oci-genai-auth](#oci-genai-auth)
  - [Table of Contents](#table-of-contents)
  - [Before You Start](#before-you-start)
  - [Installation](#installation)
  - [Examples](#examples)
    - [OCI Generative AI](#oci-generative-ai)
      - [Using the Native OpenAI Client](#using-the-native-openai-client)
      - [Using with Langchain](#using-with-langchain-openai)
    - [Google Gen AI (Gemini)](#google-gen-ai-gemini)
      - [Using the Native Google Gen AI Client](#using-the-native-google-gen-ai-client)
      - [Generate Images](#generate-images)
      - [Async Generate Content](#async-generate-content)
    - [Anthropic](#anthropic)
      - [Using the Native Anthropic Client](#using-the-native-anthropic-client)
      - [Async Messages](#async-messages)
    - [OCI Data Science Model Deployment](#oci-data-science-model-deployment)
      - [Using the Native OpenAI Client](#using-the-native-openai-client-1)
    - [Signers](#signers)
  - [Contributing](#contributing)
  - [Security](#security)
  - [License](#license)

---

## Before you start

**Important!**

This package provides OCI request-signing helpers for `httpx`. It does not ship OCI-specific SDK clients. Use the native OpenAI SDK with a custom `httpx` client that applies OCI signing.

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

- Update the `base_url` in your code:

```python
from openai import OpenAI
import os

API_KEY=os.getenv("OPENAI_API_KEY")

print(API_KEY)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1"
)

# Responses API
response = client.responses.create(
    model="openai.gpt-oss-120b",
    # model="xai.grok-3",
    # meta models are not supported with the Responses API
    input="Write a one-sentence bedtime story about a unicorn."
)
print(response)

# Completion API
response = client.chat.completions.create(
    # model="openai.gpt-oss-120b",
    # model="meta.llama-3.3-70b-instruct",
    model="xai.grok-3",
    messages=[{
        "role": "user", 
        "content": "Write a one-sentence bedtime story about a unicorn."
        }
    ]
)
print(response)
```


API Keys offer a seamless transition from code using the openai SDK, and allow usage in 3rd party code or services that don't offer an override of the http client.

However, if authentication at the user, compute instance, resource or workload level (OKE pods) is preferred, this package is for you.

It offers the same compatibility with the `openai` SDK, but requires patching the http client. See the following instruction on how to use it.

## Installation

```console
pip install oci-genai-auth
```

Install the SDKs you plan to use separately, for example:

```console
pip install openai
pip install anthropic
pip install google-genai
```

---

## Examples

### OCI Generative AI

Notes:

- **Cohere models do not support OpenAI-compatible API**
- **OCI Generative AI requires the OpenAI SDK base URL to end with `/openai/v1`**

#### Using the Native OpenAI Client

```python

import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

# Example for OCI Generative AI endpoint
client = OpenAI(
    api_key="not-used",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    http_client=httpx.Client(
        auth=OciSessionAuth(profile_name="<profile name>"),
        headers={
            "CompartmentId": "<compartment ocid>",
            "opc-compartment-id": "<compartment ocid>",
        },
    ),
)

completion = client.chat.completions.create(
    model="<model name>",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.model_dump_json())

```

If you only need the auth helpers (no OCI-specific OpenAI shim client), you can import them from
`oci_genai_auth` which only exposes the signer classes used by `httpx`.

#### Using with langchain-openai

```python
from langchain_openai import ChatOpenAI
import httpx
from oci_genai_auth import OciUserPrincipalAuth


llm = ChatOpenAI(
    model="<model name>",  # for example "xai.grok-4-fast-reasoning"
    api_key="not-used",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="<profile name>"),
        headers={
            "CompartmentId": "<compartment ocid>",
            "opc-compartment-id": "<compartment ocid>",
        },
    ),
    # use_responses_api=True
    # stream_usage=True,
    # temperature=None,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg)
```

---

### Google Gen AI (Gemini)

#### Using the Native Google Gen AI Client

```python
import httpx
from google import genai
from oci_genai_auth import OciSessionAuth

client = genai.Client(
    api_key="not-used",
    http_options={
        "base_url": "https://<your-oci-endpoint>",
        "httpx_client": httpx.Client(
            auth=OciSessionAuth(profile_name="<profile name>"),
            headers={
                "CompartmentId": "<compartment ocid>",
                "opc-compartment-id": "<compartment ocid>",
            },
        ),
    },
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Write a one-sentence bedtime story about a unicorn.",
)
print(response)
```

#### Generate Images

```python
import httpx
from google import genai
from oci_genai_auth import OciSessionAuth

client = genai.Client(
    api_key="not-used",
    http_options={
        "base_url": "https://<your-oci-endpoint>",
        "httpx_client": httpx.Client(
            auth=OciSessionAuth(profile_name="<profile name>"),
            headers={
                "CompartmentId": "<compartment ocid>",
                "opc-compartment-id": "<compartment ocid>",
            },
        ),
    },
)

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="A poster of a mythical dragon in a neon city.",
)
print(response)
```

#### Async Generate Content

```python
import asyncio

import httpx
from google import genai
from oci_genai_auth import OciSessionAuth

async def main() -> None:
    http_client = httpx.AsyncClient(
        auth=OciSessionAuth(profile_name="<profile name>"),
        headers={
            "CompartmentId": "<compartment ocid>",
            "opc-compartment-id": "<compartment ocid>",
        },
    )

    client = genai.Client(
        api_key="not-used",
        http_options={
            "base_url": "https://<your-oci-endpoint>",
            "httpx_async_client": http_client,
        },
    )

    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response)
    await http_client.aclose()

asyncio.run(main())
```

---

### Anthropic

#### Using the Native Anthropic Client

```python
import httpx
from anthropic import Anthropic
from oci_genai_auth import OciSessionAuth

client = Anthropic(
    api_key="not-used",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/anthropic",
    http_client=httpx.Client(
        auth=OciSessionAuth(profile_name="<profile name>"),
        headers={
            "CompartmentId": "<compartment ocid>",
            "opc-compartment-id": "<compartment ocid>",
        },
    ),
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=256,
    messages=[{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}],
)
print(message)
```

#### Async Messages

```python
import asyncio

import httpx
from anthropic import AsyncAnthropic
from oci_genai_auth import OciSessionAuth

async def main() -> None:
    client = AsyncAnthropic(
        api_key="not-used",
        base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/anthropic",
        http_client=httpx.AsyncClient(
            auth=OciSessionAuth(profile_name="<profile name>"),
            headers={
                "CompartmentId": "<compartment ocid>",
                "opc-compartment-id": "<compartment ocid>",
            },
        ),
    )

    message = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}],
    )
    print(message)
    await client.close()

asyncio.run(main())
```

---

### OCI Data Science Model Deployment

#### Using the Native OpenAI Client

```python

import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

# Example for OCI Data Science Model Deployment endpoint
client = OpenAI(
    api_key="not-used",
    base_url="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
    http_client=httpx.Client(auth=OciSessionAuth()),
)

response = client.chat.completions.create(
    model="<model-name>",
    messages=[
        {
            "role": "user",
            "content": "Explain how to list all files in a directory using Python.",
        },
    ],
)
print(response.model_dump_json())
```

### Signers

The library supports multiple OCI authentication methods (signers). Choose the one that matches your runtime environment and security posture.

Supported signers

- `OciSessionAuth` — Uses an OCI session token from your local OCI CLI profile.
- `OciResourcePrincipalAuth` — Uses Resource Principal auth.
- `OciInstancePrincipalAuth` — Uses Instance Principal auth. Best for OCI Compute instances with dynamic group policies.
- `OciUserPrincipalAuth` — Uses an OCI user API key. Suitable for service accounts/automation where API keys are managed securely.

Minimal examples of constructing each auth type:

```python
from oci_genai_auth import (
    OciSessionAuth,
    OciResourcePrincipalAuth,
    OciInstancePrincipalAuth,
    OciUserPrincipalAuth,
)

# 1) Session (local dev; uses ~/.oci/config + session token)
session_auth = OciSessionAuth(profile_name="DEFAULT")

# 2) Resource Principal (OCI services with RP)
rp_auth = OciResourcePrincipalAuth()

# 3) Instance Principal (OCI Compute)
ip_auth = OciInstancePrincipalAuth()

# 4) User Principal (API key in ~/.oci/config)
up_auth = OciUserPrincipalAuth(profile_name="DEFAULT")
```

---

## Contributing

This project welcomes contributions from the community.
Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md).

---

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process.

---

## License

Copyright (c) 2026 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at
[https://oss.oracle.com/licenses/upl/](https://oss.oracle.com/licenses/upl/)
