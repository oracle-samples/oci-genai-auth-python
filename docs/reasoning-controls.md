# Reasoning controls for OpenAI-compatible models

Some OCI Generative AI models deployed on a Dedicated AI Cluster support a
model-specific `enable_thinking` chat-template setting. The official OpenAI
Python SDK forwards model-specific request fields through `extra_body`.

Use this guide with either authentication option in the
[README](../README.md): OCI IAM authentication with `oci-genai-auth`, or an
OCI Generative AI API key. Replace `OCI_GENAI_MODEL_ID` with the model or
endpoint model ID configured for your deployment.

> `enable_thinking` is model and runtime dependent. Use it only when the
> deployed model's chat template supports it. Do not assume that the presence
> or absence of reasoning text in a response is a stable API contract.

## Create a client

The examples below use OCI IAM authentication. For API-key authentication,
create the same `OpenAI` client as shown in the README and omit the `http_client`.

```python
import os

import httpx
from openai import OpenAI

from oci_genai_auth import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)

model = os.environ["OCI_GENAI_MODEL_ID"]
messages = [{"role": "user", "content": "What is 15 multiplied by 37?"}]
```

## Disable thinking

For models such as Qwen whose thinking mode is enabled by default, send
`enable_thinking: false` in `chat_template_kwargs`.

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False,
        },
    },
)

print(response.choices[0].message.content)
```

## Enable thinking

When the model's chat template supports thinking mode, opt in explicitly with
`enable_thinking: true`.

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": True,
        },
    },
)

print(response.choices[0].message.content)
```

## Use the model default

Omit `chat_template_kwargs` when you want the behavior defined by the deployed
model's template and runtime.

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
)

print(response.choices[0].message.content)
```

## Use `reasoning_effort` when supported

vLLM 0.22.0 and later can map the OpenAI-compatible `reasoning_effort` field
to `enable_thinking`: `"none"` disables it, while `"low"`, `"medium"`, and
`"high"` enable it. This mapping depends on the runtime version; use the
explicit `chat_template_kwargs` examples above as the portable immediate
workaround when the deployed runtime has not been verified.

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    reasoning_effort="none",
)

print(response.choices[0].message.content)
```

Do not send conflicting values for `reasoning_effort` and
`chat_template_kwargs.enable_thinking`. When both are accepted by a runtime,
the explicit template setting is the clearest way to express the intended
model behavior.

## Further reading

- [vLLM reasoning outputs](https://docs.vllm.ai/en/latest/features/reasoning_outputs/)
- [OpenAI Python SDK undocumented request parameters](https://github.com/openai/openai-python#undocumented-request-params)
