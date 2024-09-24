from gmail2pubsub.db_init import initialize_db, load_history_id, save_history_id
from googleapiclient.errors import HttpError
from .pubsub_manager import publish_message_to_topic
from .email_parser import extract_info_from_email, extract_email_content, get_mail_sent_datetime

def get_label_id(service, label_name):
    """
    Récupère l'ID du label à partir de son nom.
    :param service: Le service API Gmail
    :param label_name: Le nom du label
    :return: L'ID du label
    """
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'] == label_name:
            return label['id']
    raise ValueError(f"Label '{label_name}' non trouvé.")

def initialize_history_id(service):
    """
    Initialise le history_id au démarrage de l'application.
    Si aucun history_id n'est trouvé dans la base de données, il est récupéré depuis Gmail.
    """
    initialize_db()  # Créer la base de données si elle n'existe pas déjà
    history_id = load_history_id()  # Charger le dernier history_id
    print(f"Loaded history_id: {history_id}")   # Debug
    if history_id is None:
        # Si aucun history_id n'est trouvé, récupère le dernier depuis Gmail
        history_id = get_last_history_id(service)
        save_history_id(history_id)  # Sauvegarde le history_id initial dans la base de données

    return history_id

def get_last_history_id(service):
    """
    Récupère l'ID de l'historique actuel du compte Gmail.
    :param service: Le service API Gmail
    :return: L'ID de l'historique
    """
    profile = service.users().getProfile(userId='me').execute()
    return int(profile['historyId'])
    
def get_new_messages(service, history_id, label_id, publisher, topic_path):
    """
    Récupère les nouveaux emails depuis un certain history_id.
    :param service: Le service API Gmail
    :param history_id: L'ID de l'historique pour commencer à récupérer les emails
    :param label_id: L'ID du label à surveiller
    :param publisher: L'instance du client Publisher pour Pub/Sub
    :param topic_path: Le chemin du topic Pub/Sub
    """
    response = service.users().history().list(
        userId='me',
        startHistoryId=str(history_id),
        historyTypes=['messageAdded'],
        labelId=label_id
    ).execute()

    history_records = response.get('history', [])
    if history_records:
        latest_history_id = history_records[-1]['id']  # Obtenir le dernier history_id

    for history_record in history_records:
        if 'messagesAdded' in history_record:
            for message in history_record['messagesAdded']:
                message_id = message['message']['id']
                extracted_info = process_message_details(service, message_id, publisher, topic_path)
                if extracted_info:
                    publish_message_to_topic(publisher, topic_path, extracted_info)

    # Sauvegarde du dernier history_id dans la base de données
    if history_records:
        save_history_id(latest_history_id)

def process_message_details(service, message_id, publisher, topic_path):
    """
    Récupère les détails d'un email à partir de son ID.
    :param service: Le service API Gmail
    :param message_id: L'ID du message à traiter
    """
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        # Récupérer la date d'envoi
        mail_sent_datetime = get_mail_sent_datetime(message)  
        email_content = extract_email_content(message)
        #print(f"Email content: {email_content}")  # Debug: Afficher le contenu complet
        #print("-------------------------------------------------")  # Debug
        extracted_info = extract_info_from_email(email_content, mail_sent_datetime)
        if extracted_info:
            publish_message_to_topic(publisher, topic_path, extracted_info)
        
    except HttpError as error:
        if error.resp.status == 404:
            return None
        else:
            raise
