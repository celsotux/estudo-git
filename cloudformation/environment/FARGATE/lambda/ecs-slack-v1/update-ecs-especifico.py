import boto3

def lambda_handler(event, context):
    try:
        # Configurações do ECS
        client = boto3.client('ecs')
        cluster_name = 'estudo-dev-cluster1'
        service_name = 'estudo-dev-app-game10'
        family = 'estudo-dev-app-game10'

        # Obtendo a revisão mais recente da definição de tarefa
        response = client.list_task_definitions(familyPrefix=family, status='ACTIVE', sort='DESC')
        if not response['taskDefinitionArns']:
            print("No active task definitions found.")
            return {"statusCode": 500, "body": "No active task definitions found."}

        new_task_definition = response['taskDefinitionArns'][0]
        print(f"New task definition: {new_task_definition}")

        # Atualizar o serviço ECS com a nova definição de tarefa
        response = client.update_service(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=new_task_definition
        )

        # Verificar se a atualização foi bem-sucedida
        if response['service']['status'] == 'ACTIVE':
            task_revision = new_task_definition.split(":")[-1]
            return {
                'statusCode': 200,
                'body': f'Serviço atualizado com sucesso para a versão {task_revision}.'
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Falha ao atualizar o serviço ECS.'
            }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}
