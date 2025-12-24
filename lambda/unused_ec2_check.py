import boto3

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[{
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }]
    )

    stopped_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])

    if stopped_instances:
        sns.publish(
            TopicArn="arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:ec2-alerts",
            Subject="Stopped EC2 Instances Found",
            Message=str(stopped_instances)
        )

    return {
        "Stopped_EC2_Instances": stopped_instances
    }
