import re
import dateutil.parser
from .utils import clean_base64_encoded_email_content
from .utils import format_phone_number, format_date_time
from datetime import datetime

def get_mail_sent_datetime(message):
    """
    Récupère la date d'envoi du mail à partir des en-têtes du message.
    :param message: Le message Gmail avec les en-têtes
    :return: Un objet datetime représentant l'heure d'envoi du mail
    """
    # Parcourir les en-têtes pour trouver le champ 'Date'
    headers = message['payload']['headers']
    mail_sent_datetime = None
    for header in headers:
        if header['name'].lower() == 'date':
            date_str = header['value']
            # Convertir la date en objet datetime
            mail_sent_datetime = dateutil.parser.parse(date_str)
            break

    if mail_sent_datetime:
        print(f"Mail sent datetime: {mail_sent_datetime}")
    else:
        print("Mail sent datetime not found")

    return mail_sent_datetime


def extract_email_content(message):
    """
    Extrait le contenu en texte brut de l'email à partir du message Gmail.
    :param message: Le message complet de l'API Gmail
    :return: Le contenu du texte de l'email (en texte brut uniquement)
    """
    email_content = ""

    if 'payload' in message:
        payload = message['payload']
        parts = payload.get('parts', [])

        # Si le mimeType est 'multipart/mixed', on doit parcourir les sous-parties
        if payload['mimeType'] == 'multipart/mixed':
            for part in parts:
                if part['mimeType'] == 'multipart/alternative':  # Rechercher les parties alternatives
                    for subpart in part.get('parts', []):
                        if subpart['mimeType'] == 'text/plain':  # Prioriser le texte brut
                            email_content += clean_base64_encoded_email_content(subpart['body']['data'])
                            break  # On arrête une fois qu'on trouve du texte brut, on ignore le HTML

        # Si le mimeType est 'multipart/alternative', pas de pièce jointe, récupérer directement
        elif payload['mimeType'] == 'multipart/alternative':
            for part in parts:
                if part['mimeType'] == 'text/plain':  # Contenu en texte brut
                    email_content += clean_base64_encoded_email_content(part['body']['data'])
                    break  # On s'arrête dès qu'on trouve du texte brut

    #print(f"email content : {email_content}")
    return email_content


def extract_info_from_email(email_content, mail_sent_datetime):
    """
    Extraction des informations du mail et détermination du type d'événement (nouveau, modifié, annulé).
    """
    email_content = re.sub(r'\r\n|\n', ' ', email_content)  # Remplacer les retours à la ligne par des espaces
    email_content = re.sub(r'\s+', ' ', email_content)  # Supprimer les espaces multiples

    extracted_info = {
        'name': 'non disponible',
        'email': 'non disponible',
        'phone': 'non disponible',
        'rdv_datetime': 'non disponible',
        'event_type': 'non disponible',
        'event_datetime': 'non disponible'
    }

    # Utiliser l'heure d'envoi du mail comme `event_datetime`
    extracted_info['event_datetime'] = mail_sent_datetime.isoformat()

    # Détection du type d'événement
    if 'Nouveau rendez-vous client' in email_content:
        extracted_info['event_type'] = 'nouveau'
        event_marker = 'Nouveau rendez-vous client'
    elif 'Rendez-vous client modifié' in email_content:
        extracted_info['event_type'] = 'modifié'
        event_marker = 'Rendez-vous client modifié'
    elif 'Rendez-vous client annulé' in email_content:
        extracted_info['event_type'] = 'annulé'
        event_marker = 'Rendez-vous client annulé'
    else:
        event_marker = None

    # Extraction de l'email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', email_content)
    if email_match:
        extracted_info['email'] = email_match.group(0)

    # Extraction du nom entre l'événement et l'email
    if event_marker and extracted_info['email'] != 'non disponible':
        name_match = re.search(rf'{event_marker}\s*(.*?)\s+{re.escape(extracted_info["email"])}', email_content)
        if name_match:
            extracted_info['name'] = name_match.group(1).strip()

    # Extraction du téléphone
    phone_match = re.search(r'(\+?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{2})', email_content)
    if phone_match:
        phone = phone_match.group(0)
        extracted_info['phone'] = format_phone_number(phone)

    # Extraction de la date et heure du rendez-vous
    date_time_match = re.search(r'📅\s*(\w+\s+\d{2}\s+\w+\s+\d{4})\s*•\s*(\d{2}:\d{2})', email_content)
    if date_time_match:
        extracted_info['rdv_datetime'] = format_date_time(date_time_match.group(1), date_time_match.group(2))

    # Extraction de la date et heure de l'annulation (s'il y a une annulation)
    cancellation_match = re.search(r'Rendez-vous annulé le\s*(\w+\s+\d{2}\s+\w+\s+\d{4})\s+à\s+(\d{2}:\d{2})', email_content)
    if cancellation_match:
        extracted_info['event_datetime'] = format_date_time(cancellation_match.group(1), cancellation_match.group(2))

    return extracted_info