import os
import json
from dotenv import load_dotenv
from iracingdataapi.client import irDataClient

# Read your .env file and loads values
load_dotenv() 

# Collect email and password from .env
email = os.getenv("IRACING_EMAIL")
password = os.getenv("IRACING_PASSWORD")

print(f"email: {email}")
print(f"password: {password}")

def get_client():

    idc = irDataClient(username=email, password=password, use_pydantic=True)

    return idc


if __name__ == "__main__":
    import hashlib
    import base64
    import requests

    # Build the hash the same way we did before
    cred = password + email.lower()
    cred_bytes = cred.encode("utf-8")
    hashed = hashlib.sha256(cred_bytes).digest()
    encoded = base64.b64encode(hashed).decode("utf-8")

    # Hit the auth endpoint directly
    session = requests.Session()
    response = session.post(
        "https://members-ng.iracing.com/auth",
        json={"email": email, "password": encoded}
    )

    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")