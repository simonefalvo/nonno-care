import boto3


def get_connection():
    # Create SQS client
    return boto3.client('sqs')


def send_message(connection, queue_url, attributes):
    # Send message to SQS queue
    response = connection.send_message(
        QueueUrl=queue_url,
        MessageAttributes=attributes,
        MessageBody=(
            'simulated event'
        )
    )
    return response
