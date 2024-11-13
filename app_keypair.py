def get_secret(secret_name):
    # Initialize a Secrets Manager client
    client = boto3.client(service_name="secretsmanager")
    # Retrieve the secret
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]

import os
import json

import boto3

from snowflake.core import Root
from snowflake.connector import connect

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

# Function to retrieve the secret from AWS Secrets Manager
def lambda_handler(event, context):
        try:
            # Retrieve the passphrase for the private key, if it exists
            private_key_passphrase = os.environ.get('PRIVATE_KEY_PASSPHRASE', None)

            # Retrieve the private key string from AWS Secrets Manager
            private_key_str = json.loads(get_secret(''))['private_key'] # add secrets manager

            # Add PEM headers and footers if they do not exist in the string
            if not private_key_str.startswith("-----BEGIN"):
                private_key_str = f"-----BEGIN PRIVATE KEY-----\n{private_key_str}\n-----END PRIVATE KEY-----"

            # Load the private key
            private_key = serialization.load_pem_private_key(
                private_key_str.encode("utf-8"),
                password=None,
                backend=default_backend()
            )
            print("Private key loaded successfully.")
        except Exception as e:
            print(f"Error loading private key: {e}")
        
        # Get Snowflake connection parameters
        connection_parameters = {
            "account": "",
            "user": "",
            "private_key": private_key,
            "role": "",
            "database": "",
            "schema": "",
        }

        svc = "" # cortex service

        print('connection parameters constructed')
        # Parse request body
        body = event
        query = body['query']
        # Validate only these columns are included in the request
        allowed_columns = ["ROOM_TYPE", "PRICE", "LISTING_TEXT", "AMENITIES", "CANCELLATION_POLICY"]
        # get the intersection of the allowed columns and the columns in the request
        columns = [col.upper() for col in body.get('columns', allowed_columns) if col in allowed_columns]
        limit = body.get('limit', 5)
        print(body)
        # Connect to Snowflake
        connection = connect(**connection_parameters)
        root = Root(connection)
        print('connected to SNOW')
        # Execute search
        response = (
            root.databases[connection_parameters["database"]]
            .schemas[connection_parameters["schema"]]
            .cortex_search_services[svc]
            .search(query, columns, limit=limit)
        )
        print(f"Received response with `request_id`: {response.request_id}")
        print(json.dumps(response.results,indent=4))
