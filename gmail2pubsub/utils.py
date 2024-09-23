import dateparser
import pytz
import base64

paris_tz = pytz.timezone('Europe/Paris')
utc_tz = pytz.UTC

def clean_base64_encoded_email_content(encoded_content):
    """
    Décode le contenu encodé en Base64URL fourni par l'API Gmail.
    :param encoded_content: Le contenu encodé
    :return: Le contenu décodé en texte brut
    """
    decoded_bytes = base64.urlsafe_b64decode(encoded_content)
    return decoded_bytes.decode('utf-8')

def format_phone_number(phone):
    """
    Convertit un numéro de téléphone au format international français.
    :param phone: Le numéro de téléphone à formater
    :return: Le numéro au format +33
    """
    phone = phone.replace(" ", "")  # Supprimer les espaces
    if phone.startswith("0"):  # Si le numéro commence par 0
        phone = "+33" + phone[1:]  # Remplacer le 0 par +33
    return phone

def format_date_time(date_str, time_str):
    """
    Convertit la date et l'heure au format ISO avec fuseau horaire UTC.
    :param date_str: La date (ex: '25 octobre 2024')
    :param time_str: L'heure (ex: '17:00')
    :return: Date/Heure au format ISO UTC
    """
    datetime_str = f"{date_str} {time_str}"
    
    # Convertir la date/heure en prenant en compte le fuseau horaire de Paris
    parsed_datetime = dateparser.parse(datetime_str, settings={'TIMEZONE': 'Europe/Paris'})
    print(f"Parsed datetime (Paris time): {parsed_datetime}")  # Debug print
    # Si la date n'a pas de fuseau horaire, appliquer celui de Paris
    if parsed_datetime.tzinfo is None:
        parsed_datetime = paris_tz.localize(parsed_datetime)
    
    else:
        print(f"Failed to parse datetime: {datetime_str}")  # Debug print
        return 'non disponible'

    # Convertir au format UTC
    utc_datetime = parsed_datetime.astimezone(utc_tz)
    print(f"Converted to UTC: {utc_datetime.isoformat()}")  # Debug print

    # Retourner la date/heure au format ISO
    return utc_datetime.isoformat()
