# Partner Examples

This folder contains partner API examples using the OpenAI Python SDK.

## Prerequisites

1. Install dependencies:

   ```bash
   pip install -e '.[dev]'
   ```

2. Configure shared values in `examples/partner/common.py`:
   - `PROFILE_NAME`
   - `COMPARTMENT_ID`
   - `REGION`

## How to run

From repository root:

```bash
python -m examples.partner.openai.quickstart_openai_chat_completions
```

## Notes

- Partner endpoints use pass-through mode and require the `opc-compartment-id` header.
- These examples use IAM signing through `oci-genai-auth`.
