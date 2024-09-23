from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from config.settings import SCOPES, TOKEN_PATH, OAUTHCRED_PATH

def authenticate_gmail_api():
    creds = None
    # Charger les credentials depuis le fichier JSON défini dans settings
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # Si les credentials sont expirés ou absents, démarrer le flux OAuth pour obtenir des tokens
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                OAUTHCRED_PATH, SCOPES)  # Utilisez un fichier OAuth si nécessaire
            creds = flow.run_local_server(port=0)

        # Sauvegarder les credentials pour un usage futur
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    # Vérification si l'authentification a été réussie
    print(f"Authenticated service account: {creds.service_account_email if hasattr(creds, 'service_account_email') else 'OAuth2 user'}")
    
    return creds
