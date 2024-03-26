import json
import urllib3

slack_url = "https://hooks.slack.com/services/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"
http = urllib3.PoolManager()

def send_slack_notification(notification):
    payload = {
        "text": notification
    }
    headers = {
        "Content-Type": "application/json"
    }
    http.request("POST", slack_url, body=json.dumps(payload), headers=headers)

def lambda_handler(event, context):
    for record in event['Records']:
        message = record['Sns']['Message']
        event_data = json.loads(message)
        if 'source' in event_data and 'eventName' in event_data:
            source = event_data['source']
            event_name = event_data['eventName']
            if source == 'aws.ec2' and event_name.startswith('RunInstances'):
                send_slack_notification("EC2 instances are starting up.")
            elif source == 'aws.ec2' and event_name.startswith('StopInstances'):
                send_slack_notification("EC2 instances are shutting down.")
            elif source == 'aws.rds' and event_name.startswith('StartDBInstance'):
                send_slack_notification("RDS instances are starting up.")
            elif source == 'aws.rds' and event_name.startswith('StopDBInstance'):
                send_slack_notification("RDS instances are shutting down.")
            elif source == 'aws.ecs' and event_name.startswith('StartTask'):
                send_slack_notification("ECS tasks are starting up.")
            elif source == 'aws.ecs' and event_name.startswith('StopTask'):
                send_slack_notification("ECS tasks are stopping.")
