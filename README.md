# Gmail2PubSub

Gmail2PubSub is an application that allows monitoring a user's emails via the Gmail API and publishing extracted information (e.g., client appointments) to Google Cloud Pub/Sub. This project supports two types of authentication: OAuth2 authentication for accessing a user's emails, and service account authentication for server-to-server interactions (Pub/Sub). The application is designed to be deployed on Kubernetes, making it easy to manage and scale.

## Project Structure

Here is an overview of the important files and folders in the project:

```bash
.
├── gmail2pubsub/
│   ├── __init__.py             # Package initialization file
│   ├── auth.py                 # OAuth2 authentication for the Gmail API
│   ├── email_parser.py         # Extracts information from emails
│   ├── gmail_manager.py        # Manages interactions with the Gmail API (labels, messages, etc.)
│   ├── main.py                 # Main script to orchestrate actions (configure watch, listen to Pub/Sub notifications, and publish information)
│   ├── main_watch.py           # Handles received Pub/Sub messages and processes related emails (callback for Pub/Sub events)
│   ├── pubsub_manager.py       # Manages publishing information to Pub/Sub
│   ├── utils.py                # Utility functions
│   ├── watch.py                # Configures push notifications on the Gmail API
├── config/
│   ├── settings.py             # Global project configuration (file paths, constants)
├── secrets/                    # Directory for secret files (service-account.json, token.json, credentials.json)
├── tests/                      # Unit tests for the project
│   ├── test_auth.py            # Tests for auth.py
│   ├── test_email_parser.py    # Tests for email_parser.py
│   ├── test_gmail_manager.py   # Tests for gmail_manager.py
│   ├── test_main.py            # Tests for main.py
│   ├── test_pubsub_manager.py  # Tests for pubsub_manager.py
│   ├── test_utils.py           # Tests for utils.py
│   ├── test_watch.py           # Tests for watch.py
├── Dockerfile                  # Configuration file for building the Docker image
├── deployment.yaml             # Configuration file for Kubernetes deployment
├── requirements.txt            # List of Python dependencies for the project
├── README.md                   # Project documentation
```

## Table of Contents

- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Command-Line Arguments](#command-line-arguments)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
  - [Kubernetes Deployment](#kubernetes-deployment)
- [Development](#development)
- [License](#license)

## Setup

### Prerequisites

- Python 3.12
- Google Cloud SDK
- Docker
- Kubernetes

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Gmail2PubSub.git
    cd Gmail2PubSub
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `secrets` directory and place your `service-account.json`, `token.json`, and `credentials.json` files inside it.

2. Update the environment variables in the `Dockerfile` and `deployment.yaml` as needed.

3. Create Kubernetes secrets:
    ```sh
    kubectl create namespace dev

    kubectl create secret generic gmail-service-account \
      --from-file=service-account.json=secrets/service-account.json \
      --namespace=dev

    kubectl create secret generic gmail-token \
      --from-file=token.json=secrets/token.json \
      --namespace=dev

    kubectl create secret generic gmail-credentials \
      --from-file=credentials.json=secrets/credentials.json \
      --namespace=dev
    ```

## Command-Line Arguments

The application supports the following command-line arguments:

- `--watch`: Configures Gmail to watch for new emails.
- `--listen`: Listens to Pub/Sub and processes incoming messages.
- `--reset-cache`: Resets the cache of the `history_id`.

Example usage:
```sh
python -m gmail2pubsub.main --watch
python -m gmail2pubsub.main --listen
python -m gmail2pubsub.main --reset-cache
```

### Running Locally

1. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```

2. Run the application:
    ```sh
    python -m gmail2pubsub.main --watch
    ```

### Running with Docker

1. Build the Docker image:
    ```sh
    docker build -t gmail2pubsub-app .
    ```
1. Push the Docker Image to a Registry:
    ```sh
    docker tag gmail2pubsub-app your-dockerhub-username/gmail2pubsub-app
    docker push your-dockerhub-username/gmail2pubsub-app
    ```  

2. Run the Docker container in the background:
    ```sh
    docker run -d \
      -e PROJECT_ID="smshttp-436212" \
      -e SUBSCRIPTION_ID="gmail-getmessages" \
      -e GMAIL_TOPIC="GmailTopic" \
      -e NEW_RDV_TOPIC="NewRdvTopic" \
      -e LABEL_NAME="RESALIB" \
      -v $(pwd)/secrets/service-account.json:/run/secrets/service-account.json \
      -v $(pwd)/secrets/token.json:/run/secrets/token.json \
      -v $(pwd)/secrets/credentials.json:/run/secrets/credentials.json \
      --name gmail2pubsub-container gmail2pubsub-app python -m gmail2pubsub.main --listen
    ```

3. Run the Docker container interactively:
    ```sh
    docker run -it \
      -e PROJECT_ID="smshttp-436212" \
      -e SUBSCRIPTION_ID="gmail-getmessages" \
      -e GMAIL_TOPIC="GmailTopic" \
      -e NEW_RDV_TOPIC="NewRdvTopic" \
      -e LABEL_NAME="RESALIB" \
      -v $(pwd)/secrets/service-account.json:/run/secrets/service-account.json \
      -v $(pwd)/secrets/token.json:/run/secrets/token.json \
      -v $(pwd)/secrets/credentials.json:/run/secrets/credentials.json \
      --name gmail2pubsub-container gmail2pubsub-app python -m gmail2pubsub.main --listen
    ```

4. To remove the Docker container:
    ```sh
    docker rm -f gmail2pubsub-container
    ```

### Kubernetes Deployment

1. Apply the ConfigMap and Deployment:
    ```sh
    kubectl apply -f configmap.yaml -n dev
    kubectl apply -f deployment.yaml -n dev
    kubectl get deployments -n dev
    ```

## Development

### Running Tests

1. Install `sqlite3`:
    ```sh
    sudo apt-get install sqlite3
    ```

2. Run the tests:
    ```sh
    pytest tests/
    ```

## License

This project is licensed under the MIT License.