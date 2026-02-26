from anthropic import Anthropic

from oci_genai_auth import OciSessionAuth
from oci_genai_auth.anthropic import OciAnthropic

client = OciAnthropic(
    auth=OciSessionAuth(profile_name="DEFAULT"),
    base_url="https://<your-oci-endpoint>",
    compartment_id="<compartment ocid>",
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=256,
    messages=[{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}],
)
print(message)