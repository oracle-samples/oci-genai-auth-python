# AgentHub Examples

This folder contains examples for OCI Generative AI AgentHub APIs using the OpenAI Python SDK.

## Prerequisites

1. Install dependencies:

   ```bash
   pip install -e '.[dev]'
   ```

2. Configure shared values in `examples/agenthub/common.py`:
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
python -m examples.agenthub.quickstart_responses_create_oci_iam
python -m examples.agenthub.quickstart_responses_create_api_key
```

Responses API examples:

```bash
python -m examples.agenthub.responses.create_response
python -m examples.agenthub.responses.streaming_text_delta
python -m examples.agenthub.responses.structured_output
python -m examples.agenthub.responses.use_gpt_model
python -m examples.agenthub.responses.use_google_gemini_model
```

Tools examples:

```bash
python -m examples.agenthub.tools.function_calling
python -m examples.agenthub.tools.web_search
python -m examples.agenthub.tools.code_interpreter
```

Other categories follow the same pattern:

```bash
python -m examples.agenthub.agents.basic_agents_example
python -m examples.agenthub.multiturn.responses_chaining
python -m examples.agenthub.memory.long_term_memory
python -m examples.agenthub.mcp.create_responses_mcp
python -m examples.agenthub.vector_stores.vector_stores_crud
python -m examples.agenthub.files.files_crud
python -m examples.agenthub.function.create_responses_fc
```

## Notes

- Most examples use IAM signing through `oci-genai-auth`.
- AgentHub examples use OpenAI-compatible `/openai/v1` endpoints and require a project OCID.
