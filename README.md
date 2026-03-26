# oci-genai-auth

[![PyPI - Version](https://img.shields.io/pypi/v/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-genai-auth.svg)](https://pypi.org/project/oci-genai-auth)

The **OCI GenAI Auth** Python library provides OCI request-signing helpers for the OpenAI-compatible REST APIs hosted by OCI Generative AI.

## Table of Contents

- [Installation](#installation)
- [Using OCI IAM Auth](#using-oci-iam-auth)
- [Using API Key Auth](#using-api-key-auth)
- [Using OCI Enterprise AI Agents APIs](#using-oci-enterprise-ai-agents-apis)
- [Examples](#examples)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Installation

```bash
pip install oci-genai-auth
```

`oci-genai-auth` is designed to work together with the official OpenAI SDK.

## Using OCI IAM Auth

Use OCI IAM auth when you want to sign requests with your OCI profile (session/user/resource/instance principal). Recommended if you are building OCI-native production workloads.

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

Use OCI Generative AI API Keys if you want a long-lived API key style auth. Recommended if you are migrating from other OpenAI-compatible API providers.

To create the OCI Generative AI API Keys, follow [this guide](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm).

You don't need to install `oci-genai-auth` if you use API key auth.

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key=os.getenv("OCI_GENAI_API_KEY"),
)
```

## Using OCI Enterprise AI Agents APIs

OCI Enterprise AI Agents provides a unified API for interacting with models and agentic capabilities.

- It is compatible with OpenAI's Responses API and the [Open Responses Spec](https://www.openresponses.org/specification), enabling developers to build agents with OpenAI SDK, OpenAI Agents SDK, LangChain, LangGraph, AI SDK, CrewAI, and more.
- It offers a uniform interface, auth, billing to access multiple model providers including OpenAI, Gemini, xAI, and GPT-OSS models hosted in OCI and your Dedicated AI Cluster.
- It provides built-in agentic primitives such as agent loop, reasoning, short-term memory, long-term memory, web search, file search, image generation, code execution, and more.

In addition to the compatible endpoint to Responses API, OCI Enterprise AI Agents also offers compatible endpoints to Files API, Vector Stores API, and Containers API.

Explore [examples](https://github.com/oracle-samples/oci-genai-auth-python/tree/main/examples/enterprise_ai_agents) to get started.

Note: OpenAI commercial models and image generation are only available to Oracle internal teams at this moment.

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

## Examples
Demo code and instructions on how to run them can be found in the ```examples``` folder.

## Contributing

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License

Copyright (c) 2026 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at https://oss.oracle.com/licenses/upl/.
