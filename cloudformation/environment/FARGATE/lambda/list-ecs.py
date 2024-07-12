import boto3
import json
import urllib3

def lambda_handler(event, context):
    try:
        # Configurações do ECS
        client = boto3.client('ecs')
        cluster_name = 'estudo-dev-cluster1'  # Nome do seu cluster
        service_name = 'estudo-dev-app-game10'  # Nome do seu serviço
        family = 'estudo-dev-app-game10'  # Nome da família da definição de tarefa
        slack_webhook_url = 'https://hooks.slack.com/services/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'

        # Obtendo a definição de tarefa atual do serviço
        response = client.describe_services(cluster=cluster_name, services=[service_name])
        if not response['services']:
            print("Service not found in the cluster.")
            return {"statusCode": 500, "body": "Service not found in the cluster."}
        
        current_task_definition = response['services'][0]['taskDefinition']
        print(f"Current task definition: {current_task_definition}")
        
        # Obtendo a revisão mais recente da definição de tarefa
        response = client.list_task_definitions(familyPrefix=family, status='ACTIVE', sort='DESC')
        print(f"Task definitions response: {response}")
        if not response['taskDefinitionArns']:
            print("No active task definitions found.")
            return {"statusCode": 500, "body": "No active task definitions found."}
        
        new_task_definition = response['taskDefinitionArns'][0]
        print(f"New task definition: {new_task_definition}")
        
        # Verificando se há uma nova revisão disponível
        if current_task_definition == new_task_definition:
            print("Nenhuma nova versão disponível.")
            return {"statusCode": 200, "body": "Nenhuma nova versão disponível."}

        # Enviar notificação para o Slack perguntando se deseja atualizar
        message = f"Nova versão disponível para o serviço `{service_name}`. Deseja atualizar?"
        slack_message = {
            "text": message,
            "attachments": [
                {
                    "text": "Clique para atualizar",
                    "fallback": "Atualização necessária",
                    "callback_id": "ecs_update",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {"name": "update", "type": "button", "text": "Atualizar", "value": "yes"}
                    ]
                }
            ]
        }
        http = urllib3.PoolManager()
        r = http.request("POST", slack_webhook_url, body=json.dumps(slack_message), headers={"Content-Type": "application/json"})
        
        # Verificar se a mensagem foi enviada com sucesso
        if r.status != 200:
            print(f"Failed to send message to Slack. Status code: {r.status}")
            return {"statusCode": r.status, "body": "Failed to send message to Slack."}
        
        # Processar a resposta do usuário
        if event.get('value') == 'yes':
            # Atualizar o serviço ECS
            response = client.update_service(cluster=cluster_name, service=service_name, taskDefinition=new_task_definition)
            # Extrair a revisão da task definition
            task_revision = new_task_definition.split(":")[-1]
            # Enviar mensagem de confirmação ao Slack
            message = f"Serviço atualizado com sucesso para a versão {task_revision}."
            slack_message = {"text": message}
            http.request("POST", slack_webhook_url, body=json.dumps(slack_message), headers={"Content-Type": "application/json"})
            return {"statusCode": 200, "body": "Service updated successfully."}
        
        return {"statusCode": 200, "body": "Waiting for user confirmation."}
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}
