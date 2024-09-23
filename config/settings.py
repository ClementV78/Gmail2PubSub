# settings.py

# OAuth 2.0 Scopes pour l'API Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Nom du projet Google Cloud et du topic Pub/Sub
PROJECT_ID = "smshttp-436212"
SUBSCRIPTION_ID = "gmail-getmessages"

# Chemin vers le fichier de credentials JSON
CREDENTIALS_PATH = "service-account.json"
TOKEN_PATH = "token.json"
# Nom du label à surveiller
LABEL_NAME = "RESALIB"

# Nom des topics Pub/Sub
GMAIL_TOPIC = "GmailTopic"  # Nom court du topic pour les notifications Gmail
NEW_RDV_TOPIC = "NewRdvTopic"  # Nom court du topic pour les rendez-vous clients