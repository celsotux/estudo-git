import boto3
import requests
from requests_aws4auth import AWS4Auth

# Configurar as credenciais e a região AWS
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
aws_region = "us-east-1"
service = "lambda"

# Configurar a autenticação AWS4
auth = AWS4Auth(credentials.access_key, credentials.secret_key, aws_region, service, session_token=credentials.token)

def lambda_handler(event):
    headers = {"Content-Type": "application/json"}
    data = {
        "status": "success",
        "repository": event["repository"],
        "version": event["version"],
        "actor": event["actor"]
    }

    response = requests.post(event["FUNCTION_URL"], json=data, headers=headers, auth=auth)
    print(response.text)

if __name__ == "__main__":
    # Exemplo de evento para testar localmente
    event = {
        "repository": "example-repo",
        "version": "11",
        "actor": "example-actor",
        "FUNCTION_URL": "https://6fray2qnjbnte5jruhxff5ijoi0huqmm.lambda-url.us-east-1.on.aws/"
    }
    lambda_handler(event)
