import argparse
from .auth import authenticate_gmail_api
from .watch import setup_gmail_watch
from .main_watch import start_pubsub_listener

def run_watch():
    # Authentification et configuration du service Gmail
    creds = authenticate_gmail_api()
    service = build('gmail', 'v1', credentials=creds)

    # Configuration du watch pour surveiller Gmail
    label_id = get_label_id(service, LABEL_NAME)
    print(f"Configuring Gmail watch for label: {label_id}")
    setup_gmail_watch(service, GMAIL_TOPIC, [label_id])

def run_pubsub_listener():
    # Lancer l'écoute sur Pub/Sub
    start_pubsub_listener()

def main():
    parser = argparse.ArgumentParser(description="Gmail2PubSub: Configure or listen to Gmail notifications.")
    parser.add_argument('--watch', action='store_true', help="Configure Gmail watch")
    parser.add_argument('--listen', action='store_true', help="Listen to Pub/Sub and publish client information")

    args = parser.parse_args()

    if args.watch:
        run_watch()
    elif args.listen:
        run_pubsub_listener()
    else:
        print("Please specify --watch or --listen")

if __name__ == '__main__':
    main()
