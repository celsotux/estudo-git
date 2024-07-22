import subprocess
import sys

# Verificar se requests-aws4auth está instalado
installed_packages = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True).stdout
if 'requests-aws4auth' not in installed_packages:
    print("requests-aws4auth não está instalado.")
else:
    print("requests-aws4auth está instalado.")

import boto3
import requests
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    # Substitua pelas suas variáveis de ambiente e credenciais AWS
    aws_region = "us-east-1"
    service = "lambda"
    access_key = "YOUR_ACCESS_KEY"
    secret_key = "YOUR_SECRET_KEY"
    session_token = "YOUR_SESSION_TOKEN"  # Se você estiver usando credenciais temporárias

    # Configure a autenticação AWS4
    auth = AWS4Auth(access_key, secret_key, aws_region, service, session_token=session_token)

    headers = {"Content-Type": "application/json"}
    data = {
        "status": "success",
        "repository": event["repository"],
        "version": event["version"],
        "actor": event["actor"]
    }

    response = requests.post(event["FUNCTION_URL"], json=data, headers=headers, auth=auth)
    print(response.text)
