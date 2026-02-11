from oci_genai_support import OciSessionAuth
from oci_genai_support.google import OciGoogleGenAI

client = OciGoogleGenAI(
    auth=OciSessionAuth(profile_name="DEFAULT"),
    base_url="https://<your-oci-endpoint>",
    compartment_id="<compartment ocid>",
)

response = client.generate_content(
    model="gemini-2.0-flash-001",
    contents="Write a one-sentence bedtime story about a unicorn.",
)
print(response)
