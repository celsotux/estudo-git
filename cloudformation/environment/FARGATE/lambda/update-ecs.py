import json
import boto3

def lambda_handler(event, context):
    try:
        # Log do evento recebido para diagnóstico
        print("Received event: " + json.dumps(event, indent=2))

        # Verificar se 'body' está presente no evento
        if 'body' in event:
            # Decodificar o corpo da solicitação
            body = json.loads(event['body'])

            # Verificar se há um payload no corpo da solicitação
            if 'payload' in body:
                payload = json.loads(body['payload'])
            else:
                raise ValueError("No payload found in request body")
        else:
            raise ValueError("Body not found in the event")

        # Verificar se há ações no payload
        if 'actions' in payload and len(payload['actions']) > 0:
            actions = payload['actions'][0]['value']
            action_details = json.loads(actions)
        else:
            raise ValueError("No actions found in payload")

        cluster_name = action_details['cluster']
        service_name = action_details['service']

        client = boto3.client('ecs')

        # Obter a última revisão disponível
        task_definitions = client.list_task_definitions(
            familyPrefix=service_name,
            status='ACTIVE',
            sort='DESC'
        )

        if 'taskDefinitionArns' in task_definitions and len(task_definitions['taskDefinitionArns']) > 0:
            latest_revision_arn = task_definitions['taskDefinitionArns'][0]

            # Atualizar o serviço para usar a última revisão
            client.update_service(
                cluster=cluster_name,
                service=service_name,
                taskDefinition=latest_revision_arn
            )
        else:
            raise ValueError("No active task definitions found")

        return {
            'statusCode': 200,
            'body': json.dumps('Service updated successfully')
        }

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
