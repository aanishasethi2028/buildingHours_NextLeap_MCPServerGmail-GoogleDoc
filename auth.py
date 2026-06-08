import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.compose",
]


def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth2 flow."""
    creds = None
    
    # Check if token is in environment variables
    token_json_str = os.environ.get("GOOGLE_TOKEN_JSON")
    if token_json_str:
        token_info = json.loads(token_json_str)
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    # Fallback to local token.json
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secret_str = os.environ.get("GOOGLE_CLIENT_SECRET_JSON")
            if client_secret_str:
                client_config = json.loads(client_secret_str)
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            elif os.path.exists("client_secret.json"):
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json", SCOPES
                )
            else:
                raise FileNotFoundError(
                    "Client secret not found. Set GOOGLE_CLIENT_SECRET_JSON env var or "
                    "place client_secret.json in the directory."
                )
            
            # This requires user interaction, will fail on PaaS without a browser
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds
