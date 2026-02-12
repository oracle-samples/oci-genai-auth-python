from oci_genai_auth import OciSessionAuth
from oci_genai_auth.google import OciGoogleGenAI

client = OciGoogleGenAI(
    auth=OciSessionAuth(profile_name="DEFAULT"),
    base_url="https://<your-oci-endpoint>",
    compartment_id="<compartment ocid>",
)

response = client.generate_images(
    model="imagen-3.0-generate-002",
    prompt="A poster of a mythical dragon in a neon city.",
)
print(response)
