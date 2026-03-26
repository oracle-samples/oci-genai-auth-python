# OCI Enterprise AI Agents Examples

This folder contains examples for OCI Enterprise AI Agents APIs using the OpenAI Python SDK.

## Prerequisites

1. Install dependencies:

   ```bash
   pip install -e '.[dev]'
   ```

2. Configure shared values in `examples/enterprise_ai_agents/common.py`:
   - `PROFILE_NAME`
   - `COMPARTMENT_ID`
   - `PROJECT_OCID`
   - `REGION`

3. (Optional) You can override project at runtime:

   ```bash
   export OCI_GENAI_PROJECT_ID=<your_project_ocid>
   ```

4. If running API-key based examples, set:

   ```bash
   export OPENAI_API_KEY=<your_oci_genai_api_key>
   ```

## How to run

From repository root, run any example module with `python -m`.

Quickstarts:

```bash
python -m examples.enterprise_ai_agents.quickstart_responses_create_oci_iam
python -m examples.enterprise_ai_agents.quickstart_responses_create_api_key
```

Responses API examples:

```bash
python -m examples.enterprise_ai_agents.responses.create_response
python -m examples.enterprise_ai_agents.responses.streaming_text_delta
python -m examples.enterprise_ai_agents.responses.structured_output
python -m examples.enterprise_ai_agents.responses.use_gpt_model
python -m examples.enterprise_ai_agents.responses.use_google_gemini_model
```

Tools examples:

```bash
python -m examples.enterprise_ai_agents.tools.function_calling
python -m examples.enterprise_ai_agents.tools.web_search
python -m examples.enterprise_ai_agents.tools.code_interpreter
```

Other categories follow the same pattern:

```bash
python -m examples.enterprise_ai_agents.agents.basic_agents_example
python -m examples.enterprise_ai_agents.multiturn.responses_chaining
python -m examples.enterprise_ai_agents.memory.long_term_memory
python -m examples.enterprise_ai_agents.mcp.create_responses_mcp
python -m examples.enterprise_ai_agents.vector_stores.vector_stores_crud
python -m examples.enterprise_ai_agents.files.files_crud
python -m examples.enterprise_ai_agents.function.create_responses_fc
```

## Notes

- Most examples use IAM signing through `oci-genai-auth`.
- OCI Enterprise AI Agents examples use OpenAI-compatible `/openai/v1` endpoints and require a project OCID.
