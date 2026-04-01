import os
import json
import requests
import hashlib
import base64
from dotenv import load_dotenv

# Read your .env file and loads values
load_dotenv() 

# Collect email and password
email = os.getenv("IRACING_EMAIL")
password = os.getenv("IRACING_PASSWORD")

# Create credentials for iRacing, hash, Base64 encode it and then decode back to UTF-8 
cred = password + email.lower()
cred_bytes = cred.encode("utf-8")
hashed_cred = hashlib.sha256(cred_bytes).digest()
encoded_cred = base64.b64encode(hashed_cred).decode("utf-8")

print(f"email: {email}")
print(f"password: {password}")
print(f"encoded_cred: {encoded_cred}")

def get_session(userEmail, userCred):
    session = requests.Session()

    response = session.post(
        "https://oauth.iracing.com/oauth2/token",
        json={
            "grant_type": "password", 
            "email": userEmail, 
            "password": userCred}
    )   

    print(f"Auth status: {response.status_code}")
    print(f"Auth response: {response.json()}")

    print("Connected!")
    return session


if __name__ == "__main__":
    session = get_session(email, encoded_cred)
    print(f"Session type: {type(session)}")