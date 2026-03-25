# Migration Guide: `oci-openai` to `oci-genai-auth`

This guide helps existing `oci-openai` users migrate to `oci-genai-auth`.

## Summary

- Replace dependency `oci-openai` with `oci-genai-auth`.
- Continue using the `openai` Python SDK client.
- Use `OciSessionAuth` to sign requests with OCI IAM.
- Use endpoint `https://inference.generativeai.<region>.oci.oraclecloud.com/openai/v1` with a `project` OCID.

## 1) Dependency Changes

Uninstall old package and install the new one:

```bash
pip uninstall -y oci-openai
pip install oci-genai-auth openai
```

If you pin dependencies, update your requirements file accordingly.

## 2) Import Changes

```python
from oci_openai import OciSessionAuth
```

## 3) Client Initialization Changes

Use the OpenAI-compatible endpoint and provide project OCID:

```python
import httpx
from openai import OpenAI
from oci_genai_auth import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.<region>.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    project="<ocid1.generativeaiproject...>",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)
```

## 4) Endpoint and required parameters

- `base_url`: `https://inference.generativeai.<region>.oci.oraclecloud.com/openai/v1`
- required: `project=<PROJECT_OCID>`
