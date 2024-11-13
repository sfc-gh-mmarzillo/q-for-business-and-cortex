import os
import json
import boto3
from snowflake.core import Root
from snowflake.connector import connect
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from cryptography.hazmat.primitives import serialization

# Function to retrieve the secret from AWS Secrets Manager
def lambda_handler(event, context):
    # Get Snowflake connection parameters
    connection_parameters = {
        "account": "",
        "user": "",
        "password": "",
        "role": "ACCOUNTADMIN",
        "database": "cortex_search_tutorial_db",
        "schema": "PUBLIC",
    }

    svc = "airbnb_svc"

    # Parse request body
    body = event
    query = body['query']
    
    # Validate only these columns are included in the request
    allowed_columns = ["ROOM_TYPE", "PRICE", "LISTING_TEXT", "AMENITIES", "CANCELLATION_POLICY"]
    # Get the intersection of the allowed columns and the columns in the request
    columns = [col.upper() for col in body.get('columns', allowed_columns) if col.upper() in allowed_columns]
    limit = body.get('limit', 5)

    try:
        # Connect to Snowflake
        connection = connect(**connection_parameters)
        root = Root(connection)
        
        # Execute search
        response = (
            root.databases[connection_parameters["database"]]
            .schemas[connection_parameters["schema"]]
            .cortex_search_services[svc]
            .search(query, columns, limit=limit)
        )

        print(f"Received response with `request_id`: {response.request_id}")
        print(json.dumps(response.results, indent=4))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'request_id': response.request_id,
                'results': response.results,
            }),
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
        }
    finally:
        if 'connection' in locals():
            connection.close()
