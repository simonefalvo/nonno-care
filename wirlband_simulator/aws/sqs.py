import boto3


def send_message(queue_url, attributes):

    # Create SQS client
    sqs = boto3.client('sqs')

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes=attributes,
        MessageBody=(
            'simulated event'
        )
    )

    print(response['MessageId'])
