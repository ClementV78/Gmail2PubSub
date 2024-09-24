# Utiliser une image Python légère
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Variable d'environnement par défaut (modifiables via Docker)
ENV PROJECT_ID="smshttp-436212"
ENV SUBSCRIPTION_ID="gmail-getmessages"
ENV CREDENTIALS_PATH="/run/secrets/service-account.json"
ENV TOKEN_PATH="/run/secrets/token.json"
ENV OAUTHCRED_PATH="/run/secrets/credentials.json"
ENV LABEL_NAME="RESALIB"
ENV GMAIL_TOPIC="GmailTopic"
ENV NEW_RDV_TOPIC="NewRdvTopic"
# Désactiver le buffering pour s'assurer que les logs s'affichent immédiatement
ENV PYTHONUNBUFFERED=1

# Exécuter l'application (remplacer par la commande principale de votre script)
CMD ["python", "-m", "gmail2pubsub.main"]
