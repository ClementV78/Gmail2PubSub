from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import shutil
from config.settings import SCOPES, TOKEN_PATH, OAUTHCRED_PATH

# Define a writable path for the token
WRITABLE_TOKEN_PATH = '/app/writable_token.json'

def authenticate_gmail_api():
    creds = None

    # Copy the token file to a writable location if it exists
    if os.path.exists(TOKEN_PATH):
        shutil.copy(TOKEN_PATH, WRITABLE_TOKEN_PATH)

    # Load credentials from the writable token path
    if os.path.exists(WRITABLE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(WRITABLE_TOKEN_PATH, SCOPES)
    
    # If credentials are expired or absent, start the OAuth flow to obtain tokens
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                OAUTHCRED_PATH, SCOPES)  # Use an OAuth file if necessary
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(WRITABLE_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    
    # Vérification si l'authentification a été réussie
    print(f"Authenticated service account: {creds.service_account_email if hasattr(creds, 'service_account_email') else 'OAuth2 user'}")
  
    return creds