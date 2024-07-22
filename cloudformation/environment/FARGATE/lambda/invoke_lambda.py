import boto3
import requests
from requests.auth import AWS4Auth
import os

region = os.environ['AWS_REGION']
service = 'lambda'
credentials = boto3.Session().get_credentials()
auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

headers = {"Content-Type": "application/json"}
data = {
    "status": "success",
    "repository": os.environ['REPOSITORY_NAME'],
    "version": os.environ['IMAGE_VERSION'],
    "actor": os.environ['GITHUB_ACTOR']
}

response = requests.post(os.environ['FUNCTION_URL'], json=data, headers=headers, auth=auth)
print(response.text)
