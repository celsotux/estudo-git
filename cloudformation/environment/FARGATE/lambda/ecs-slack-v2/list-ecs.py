import boto3
import json
import urllib3

def lambda_handler(event, context):
    try:
        # Configurações do ECS
        client = boto3.client('ecs')
        slack_webhook_url = 'https://hooks.slack.com/services/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'

        # Listando todos os clusters
        clusters = client.list_clusters()['clusterArns']
        print(f"Clusters: {clusters}")

        for cluster_arn in clusters:
            # Listando todos os serviços no cluster
            services = client.list_services(cluster=cluster_arn)['serviceArns']
            print(f"Services in {cluster_arn}: {services}")

            for service_arn in services:
                try:
                    # Obtendo a definição de tarefa atual do serviço
                    response = client.describe_services(cluster=cluster_arn, services=[service_arn])
                    if not response['services']:
                        print(f"Service not found in the cluster: {service_arn}")
                        continue

                    current_task_definition = response['services'][0]['taskDefinition']
                    current_revision = current_task_definition.split(':')[-1]
                    print(f"Current task definition: {current_task_definition} (Revision: {current_revision})")

                    # Obtendo a família da tarefa atual
                    task_definition = client.describe_task_definition(taskDefinition=current_task_definition)
                    family = task_definition['taskDefinition']['family']
                    print(f"Family: {family}")

                    # Obtendo o nome do serviço a partir da ARN
                    service_name = service_arn.split('/')[-1]
                    print(f"Service name: {service_name}")

                    # Obtendo a revisão mais recente da definição de tarefa
                    response = client.list_task_definitions(familyPrefix=family, status='ACTIVE', sort='DESC')
                    if not response['taskDefinitionArns']:
                        print(f"No active task definitions found for family: {family}")
                        continue

                    new_task_definition = response['taskDefinitionArns'][0]
                    new_revision = new_task_definition.split(':')[-1]
                    print(f"New task definition: {new_task_definition} (Revision: {new_revision})")

                    # Verificando se há uma nova revisão disponível
                    if current_task_definition == new_task_definition:
                        print(f"Nenhuma nova versão disponível para o serviço: {service_name}")
                        continue

                    # Enviar notificação para o Slack perguntando se deseja atualizar
                    message = (f"Nova versão disponível para o serviço `{service_name}`. "
                               f"Revisão atual: {current_revision}. Nova revisão: {new_revision}. Deseja atualizar?")
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
                                    {"name": "update", "type": "button", "text": "Atualizar", "value": service_name}
                                ]
                            }
                        ]
                    }
                    http = urllib3.PoolManager()
                    r = http.request("POST", slack_webhook_url, body=json.dumps(slack_message), headers={"Content-Type": "application/json"})

                    # Verificar se a mensagem foi enviada com sucesso
                    if r.status != 200:
                        print(f"Failed to send message to Slack for service {service_name}. Status code: {r.status}")
                        continue

                except Exception as e:
                    print(f"An error occurred while processing service {service_name}: {str(e)}")
                    continue

        # Se a mensagem foi enviada com sucesso, retornar status 200
        return {"statusCode": 200, "body": "Mensagem enviada para o Slack com o botão de atualização."}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}
