# Gmail2PubSub

Gmail2PubSub est une application qui permet de surveiller les emails d'un utilisateur via l'API Gmail et de publier les informations extraites (par exemple, les rendez-vous clients) sur Google Cloud Pub/Sub. Ce projet supporte deux types d'authentification : l'authentification OAuth2 pour l'accès aux emails d'un utilisateur, et l'authentification via un compte de service pour les interactions serveur à serveur (Pub/Sub).

## Structure du projet

Voici un aperçu des fichiers et dossiers importants du projet :

```bash
.
├── gmail2pubsub/
│   ├── __init__.py             # Fichier d'initialisation du package
│   ├── auth.py                 # Authentification OAuth2 pour l'API Gmail
│   ├── email_parser.py         # Extraction des informations des emails
│   ├── gmail_manager.py        # Gestion de l'API Gmail (labels, messages, etc.)
│   ├── main.py                 # Script principal pour orchestrer les actions (configurer le watch, écouter les notifications Pub/Sub et publier les informations)
│   ├── main_watch.py           # Gestion des messages Pub/Sub reçus et traitement des emails liés (callback pour les événements Pub/Sub)
│   ├── pubsub_manager.py       # Gestion de la publication des informations sur Pub/Sub
│   ├── utils.py                # Fonctions utilitaires
│   ├── watch.py                # Configuration des notifications push sur l'API Gmail
├── config/
│   ├── settings.py             # Configuration globale du projet (chemins des fichiers, constantes)
├── token.json                  # Jetons OAuth2 pour l'accès à l'API Gmail d'un utilisateur
├── credentials.json            # Fichier de configuration OAuth2 (client secrets) pour l'utilisateur
├── service-account.json        # Informations d'authentification pour le compte de service Google Cloud
├── requirements.txt            # Dépendances du projet
├── README.md                   # Ce fichier
├── setup.py                    # Script pour installer les dépendances via setuptools
├── tests/                      # Tests unitaires
│   ├── test_gmail_manager.py    # Tests pour le gestionnaire Gmail
│   ├── test_pubsub_manager.py   # Tests pour la gestion de Pub/Sub


## Prérequis
- **Python 3.8 ou supérieur**
- **Un compte Google Cloud** avec accès à l'API Gmail et Pub/Sub
- **Un projet Google Cloud** configuré avec Pub/Sub et un compte de service avec les permissions nécessaires

## Fichiers JSON

### 1. `service-account.json`
- **Description** : Ce fichier contient les informations d'authentification d'un compte de service Google Cloud. Il permet à l'application d'agir comme un service pour accéder à Pub/Sub.
- **Usage** : Il est utilisé pour interagir avec Google Pub/Sub pour publier et écouter des messages. Il est référencé via `CREDENTIALS_PATH`.

### 2. `credentials.json`
- **Description** : Ce fichier est utilisé pour l'authentification OAuth2 d'un utilisateur spécifique. Il contient les informations du client (client ID, client secret) pour démarrer le flux OAuth2.
- **Usage** : Il est utilisé lors de la première connexion pour authentifier l'utilisateur via le flux OAuth et obtenir les jetons nécessaires pour accéder à ses emails via l'API Gmail.

### 3. `token.json`
- **Description** : Ce fichier contient les jetons d'authentification OAuth2 (jetons d'accès et de rafraîchissement) pour accéder aux emails de l'utilisateur. Il est généré après l'authentification initiale.
- **Usage** : Il est utilisé pour les appels ultérieurs à l'API Gmail sans nécessiter de nouvelle authentification. Il est référencé via `TOKEN_PATH` dans le fichier de configuration.

## Configuration

### 1. Activer les APIs nécessaires :
- Activez l'API Gmail et l'API Pub/Sub sur Google Cloud pour votre projet.

### 2. Configurer un compte de service :
- Créez un compte de service sur Google Cloud et téléchargez le fichier `service-account.json` dans la racine de votre projet.

### 3. Configurer l'authentification OAuth2 :
- Obtenez les informations OAuth2 (client ID et client secret) via la [Console des API Google](https://console.cloud.google.com/apis/credentials) et enregistrez-les dans `credentials.json`.

### 4. Installer les dépendances :
Installez les dépendances avec pip :

```bash
pip install -r requirements.txt

## Utilisation

### 1. Configurer le watch sur Gmail
Le watch sur Gmail configure les notifications push pour surveiller les nouveaux emails et déclencher un message sur Pub/Sub lorsque de nouveaux emails arrivent.

```bash
python -m gmail2pubsub.main --watch

## 2. Écouter les notifications Pub/Sub et publier les informations client
Cette commande écoute les messages sur le topic Pub/Sub et publie les informations extraites (nom, téléphone, rendez-vous, etc.) sur un autre topic.

```bash
python -m gmail2pubsub.main --listen


## Variables et Configuration dans `settings.py`

- **PROJECT_ID** : L'identifiant du projet Google Cloud.
- **SUBSCRIPTION_ID** : L'ID de la souscription Pub/Sub.
- **GMAIL_TOPIC** : Le topic Pub/Sub où Gmail envoie les notifications.
- **NEW_RDV_TOPIC** : Le topic Pub/Sub où les informations des rendez-vous sont publiées.
- **SCOPES** : Les scopes OAuth2 pour l'API Gmail.
- **CREDENTIALS_PATH** : Le chemin vers le fichier `service-account.json`.
- **TOKEN_PATH** : Le chemin vers le fichier `token.json`.

## Tests
Les tests unitaires peuvent être lancés avec `pytest` :

```bash
pytest tests/


Secrets Kubernetes
 kubectl create namespace dev

 kubectl create secret generic gmail-service-account \
  --from-file=service-account.json=service-account.json \
  --namespace=dev
secret/gmail-service-account created

kubectl create secret generic gmail-token \
  --from-file=token.json=token.json \
  --namespace=dev
secret/gmail-token created

kubectl create secret generic gmail-credentials \
  --from-file=credentials.json=credentials.json \
  --namespace=dev
secret/gmail-credentials created

venv :
source ~/projetsperso/smsgwy/venv/bin/activate

python -m gmail2pubsub.main --listen


docker build -t gmail2pubsub-app .\n

Lancer le conteneur Docker en arrière-plan :
docker run -d \
  -e PROJECT_ID="smshttp-436212" \
  -e SUBSCRIPTION_ID="gmail-getmessages" \
  -e GMAIL_TOPIC="GmailTopic" \
  -e NEW_RDV_TOPIC="NewRdvTopic" \
  -e LABEL_NAME="RESALIB" \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/secrets/service-account.json:/run/secrets/service-account.json \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/secrets/token.json:/run/secrets/token.json \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/credentials.json:/run/secrets/credentials.json \
  --name gmail2pubsub-container gmail2pubsub-app python -m gmail2pubsub.main --listen

Lancer le conteneur Docker en mode interactif :
  docker run -it \
  -e PROJECT_ID="smshttp-436212" \
  -e SUBSCRIPTION_ID="gmail-getmessages" \
  -e GMAIL_TOPIC="GmailTopic" \
  -e NEW_RDV_TOPIC="NewRdvTopic" \
  -e LABEL_NAME="RESALIB" \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/secrets/service-account.json:/run/secrets/service-account.json \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/secrets/token.json:/run/secrets/token.json \
  -v /home/xclem/projetsperso/smsgwy/gcp/Gmail2PubSub/credentials.json:/run/secrets/credentials.json \
  --name gmail2pubsub-container gmail2pubsub-app python -m gmail2pubsub.main --listen

#Pour supprimer
docker rm -f gmail2pubsub-container

## License
Ce projet est sous licence MIT.
