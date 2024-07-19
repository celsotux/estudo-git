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

        updated_services = []

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

                    # Atualizar o serviço ECS com a nova definição de tarefa
                    response = client.update_service(
                        cluster=cluster_arn,
                        service=service_arn,
                        taskDefinition=new_task_definition
                    )

                    # Verificar se a atualização foi bem-sucedida
                    if response['service']['status'] == 'ACTIVE':
                        updated_services.append((service_name, current_revision, new_revision))
                        print(f'Serviço {service_name} atualizado com sucesso para a versão {new_revision}.')
                    else:
                        print(f'Falha ao atualizar o serviço {service_name}.')

                except Exception as e:
                    print(f"An error occurred while updating service {service_name}: {str(e)}")
                    continue

        # Enviar notificação para o Slack apenas com os nomes dos serviços atualizados
        if updated_services:
            updates = [f"{service} (de {current} para {new})" for service, current, new in updated_services]
            message = f"Serviços atualizados com sucesso: {', '.join(updates)}"
            slack_message = {
                "text": message
            }
            http = urllib3.PoolManager()
            r = http.request("POST", slack_webhook_url, body=json.dumps(slack_message), headers={"Content-Type": "application/json"})

            # Verificar se a mensagem foi enviada com sucesso
            if r.status != 200:
                print(f"Failed to send message to Slack. Status code: {r.status}")
                return {"statusCode": r.status, "body": "Failed to send message to Slack."}

        # Se nenhum serviço foi atualizado, retornar uma mensagem indicando isso
        else:
            return {
                'statusCode': 200,
                'body': 'Nenhum serviço foi atualizado.'
            }

        # Se a mensagem foi enviada com sucesso, retornar status 200
        return {"statusCode": 200, "body": "Mensagem enviada para o Slack com os serviços atualizados."}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}
