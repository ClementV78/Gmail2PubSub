from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound, AlreadyExists
import json

def create_topic_if_not_exists(publisher, topic_path):
    """
    Crée un topic Pub/Sub seulement s'il n'existe pas déjà.
    :param publisher: L'instance du client Publisher
    :param topic_path: Le chemin complet du topic Pub/Sub
    """
    try:
        print(f"Création du topic '{topic_path}'")
        publisher.create_topic(name=topic_path)
        # print(f"Topic '{topic_path}' créé avec succès.")  # Debug
    except AlreadyExists:
        # print(f"Le topic '{topic_path}' existe déjà.")  # Debug
        pass

def publish_message_to_topic(publisher, topic_path, message):
    """
    Publie un message dans un topic Pub/Sub.
    :param publisher: L'instance du client Publisher
    :param topic_path: Le chemin complet du topic Pub/Sub
    :param message: Le message à publier (dictionnaire Python)
    """
    try:
        # Tente de publier le message
        print(f"Tentative de publication du message ' {message} ' dans le topic '{topic_path}'")  # Message important
        future = publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
        future.result()  # Assure que le message est bien publié
        print(f"Message publié dans le topic '{topic_path}'")  # Message important
    except NotFound:
        # Si le topic n'existe pas, le créer, puis republier
        create_topic_if_not_exists(publisher, topic_path)
        # Réessayer de publier après la création du topic
        future = publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
        future.result()
        print(f"Message publié dans le topic '{topic_path}' après création")
