from google.cloud import pubsub_v1
from google.oauth2 import service_account
from .gmail_manager import get_new_messages, get_last_history_id, get_label_id
from .auth import authenticate_gmail_api
from googleapiclient.discovery import build
from config.settings import PROJECT_ID, SUBSCRIPTION_ID, NEW_RDV_TOPIC, CREDENTIALS_PATH, LABEL_NAME
import json

# Initialiser Pub/Sub et authentifier avec le compte de service
def start_pubsub_listener():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    topic_path = publisher.topic_path(PROJECT_ID, NEW_RDV_TOPIC)

    # Initialisation du last_history_id et label_id
    creds = authenticate_gmail_api()
    service = build('gmail', 'v1', credentials=creds)
    last_history_id = get_last_history_id(service)
    label_id = get_label_id(service, LABEL_NAME)

    # Fonction callback pour traiter les messages
    def callback(message):
        nonlocal last_history_id

        print(f"Received message: {message.data}")
        message.ack()

        data = json.loads(message.data.decode('utf-8'))
        history_id = int(data['historyId'])

        if history_id > last_history_id:
            get_new_messages(service, last_history_id, label_id, publisher, topic_path)
            last_history_id = history_id

    # Écouter les messages sur Pub/Sub
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
