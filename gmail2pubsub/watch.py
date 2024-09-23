# watch.py

from googleapiclient.discovery import build
from .auth import authenticate_gmail_api
from .gmail_manager import get_label_id
from config.settings import PROJECT_ID, GMAIL_TOPIC, LABEL_NAME



# Fonction pour configurer le watch
def setup_gmail_watch(service, topic_name, label_ids):
    full_topic_name = f"projects/{PROJECT_ID}/topics/{topic_name}"  # Assurer le format correct ici
    request_body = {
        'labelIds': label_ids,  
        'labelFilterBehavior': 'INCLUDE',  
        'topicName': full_topic_name  # Utilise le nom complet du topic
    }

    response = service.users().watch(userId='me', body=request_body).execute()
    print('Watch response:', response)

def main():
    # Authentification via OAuth 2.0
    creds = authenticate_gmail_api()
    service = build('gmail', 'v1', credentials=creds)

    # Récupération de l'ID du label à partir du nom (par ex. 'RESALIB')
    label_id = get_label_id(service, LABEL_NAME)

    # Configuration du watch sur Gmail
    setup_gmail_watch(service, GMAIL_TOPIC, [label_id])

if __name__ == '__main__':
    main()
