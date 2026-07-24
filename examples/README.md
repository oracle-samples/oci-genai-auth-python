# OCI Generative AI SDK Quickstarts

This folder contains quickstarts for the supported OpenAI-compatible APIs and auth modes:

- Responses API with OCI Generative AI API Key auth
- Responses API with OCI IAM auth through `oci-genai-auth`
- Chat Completions API with OCI Generative AI API Key auth, sync and async
- Chat Completions API with OCI IAM auth through `oci-genai-auth`, sync and async
- Google Gen AI SDK with OCI Generative AI API-key and OCI IAM authentication

## Prerequisites

1. Install dependencies:

   ```bash
   pip install -e '.[examples]'
   ```

2. Configure shared values in `examples/common.py`:
   - `PROFILE_NAME`
   - `PROJECT_OCID`
   - `REGION`

3. (Optional) You can override shared values at runtime:

   ```bash
   export OCI_GENAI_PROFILE=<your_oci_profile>
   export OCI_GENAI_REGION=<your_region>
   export OCI_GENAI_PROJECT_ID=<your_project_ocid>
   export OCI_GENAI_RESPONSES_MODEL=<your_responses_model>
   export OCI_GENAI_CHAT_MODEL=<your_chat_model>
   ```

4. If running API-key based examples, set:

   ```bash
   export OPENAI_API_KEY=<your_openai_compatible_oci_genai_api_key>
   export OCI_GENAI_API_KEY=<your_google_compatible_oci_genai_api_key>
   ```

5. If running OCI IAM Chat Completions examples, set:

   ```bash
   export OCI_GENAI_COMPARTMENT_ID=<your_compartment_ocid>
   ```

## How to run

From repository root, run any example module with `python -m`.

Quickstarts:

```bash
python -m examples.quickstart_responses_create_oci_iam
python -m examples.quickstart_responses_create_api_key
python -m examples.quickstart_chat_completions_create_oci_iam
python -m examples.quickstart_chat_completions_create_oci_iam_async
python -m examples.quickstart_chat_completions_create_api_key
python -m examples.quickstart_chat_completions_create_api_key_async
python -m examples.google.generate_content_api_key
python -m examples.google.generate_content_oci_iam
python -m examples.google.generate_content_oci_iam_async
```

## Notes

- API-key quickstarts use `OPENAI_API_KEY` and do not require `oci-genai-auth` for auth.
- OCI IAM quickstarts use `oci-genai-auth` with the OpenAI SDK.
- OCI IAM Chat Completions quickstarts pass `COMPARTMENT_ID` as both `CompartmentId` and `opc-compartment-id` headers.
- Chat Completions defaults to `meta.llama-4-scout-17b-16e-instruct`; override `OCI_GENAI_CHAT_MODEL` if needed.
- These quickstarts use OCI Generative AI OpenAI-compatible `/openai/v1` endpoints and require a project OCID.
- Google Gen AI quickstarts use the OCI Generative AI `/google` endpoint. API-key examples use `OCI_GENAI_API_KEY`; OCI IAM examples need a valid OCI CLI session/profile.
