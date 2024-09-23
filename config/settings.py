import os

# OAuth 2.0 Scopes pour l'API Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Paramètres modifiables par environnement
PROJECT_ID = os.getenv('PROJECT_ID', 'smshttp-436212')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID', 'gmail-getmessages')

# Détection de l'environnement Kubernetes vs local
if os.path.exists('/secrets/service-account.json'):
    CREDENTIALS_PATH = '/secrets/service-account.json'
    TOKEN_PATH = '/secrets/token.json'
    OAUTHCRED_PATH = '/secrets/credentials.json'
else:
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'secrets/service-account.json')
    TOKEN_PATH = os.getenv('TOKEN_PATH', 'secrets/token.json')
    OAUTHCRED_PATH = os.getenv('OAUTH2_PATH', 'secrets/credentials.json')

# Nom du label à surveiller
LABEL_NAME = os.getenv('LABEL_NAME', 'RESALIB')

# Nom des topics Pub/Sub
GMAIL_TOPIC = os.getenv('GMAIL_TOPIC', 'GmailTopic')
NEW_RDV_TOPIC = os.getenv('NEW_RDV_TOPIC', 'NewRdvTopic')
