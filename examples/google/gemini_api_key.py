import os

from oci_genai_auth.google import OciGoogleGenAI

client = OciGoogleGenAI(
    auth=None,
    base_url="https://<google-genai-base-url>",
    vertexai=False,
    api_key=os.getenv("GEMINI_API_KEY"),
)

response = client.generate_content(
    model="gemini-2.0-flash-001",
    contents="Summarize the benefits of using OCI with Gemini models.",
)
print(response)
