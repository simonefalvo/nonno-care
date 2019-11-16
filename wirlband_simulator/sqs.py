import boto3
import time


def send_message(user, queue_url, fall_data=None, sos=None):

    timestamp = time.time()

    # Create SQS client
    sqs = boto3.client('sqs')

    attributes = {
        'sensor_id': {
            'DataType': 'Number',
            'StringValue': str(user.sensor_id)
        },
        'timestamp': {
            'DataType': 'String',
            'StringValue': str(timestamp)
        },
        'latitude': {
            'DataType': 'Number.float',
            'StringValue': str(user.current_latitude)
        },
        'longitude': {
            'DataType': 'Number.float',
            'StringValue': str(user.current_longitude)
        },
        'heart_rate': {
            'DataType': 'Number',
            'StringValue': str(user.current_hrate())
        }
    }

    if fall_data is not None:
        attributes['fall_data'] = {
                'DataType': 'String',
                'StringValue': fall_data
            }

    if sos is not None:
        attributes['sos'] = {
                'DataType': 'String',
                'StringValue': '1'
            }

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes=attributes,
        MessageBody=(
            'simulated event'
        )
    )

    print(response['MessageId'])
