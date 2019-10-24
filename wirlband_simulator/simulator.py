import boto3
import time
import random


PERIOD = 120  # Sample period


if __name__ == '__main__':

    # Create SQS client
    sqs = boto3.client('sqs')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('nonno-stack-UserDataTable-RMJMKMKYK11F')

    queue_url = "https://sqs.eu-west-3.amazonaws.com/043090642581/nonno-stack-nonnoSqsQueue-WXX8HD7VM1G6"

    sensor_id = 2
    avg_freq = random.randint(60, 100)

    while True:
        timestamp = time.time()
        latitude = 41.858362
        longitude = 12.635893
        heart_rate = 102

        # Create user data info

        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'sensor_id': {
                    'DataType': 'Number',
                    'StringValue': str(sensor_id)
                },
                'timestamp': {
                    'DataType': 'String',
                    'StringValue': str(timestamp)
                },
                'latitude': {
                    'DataType': 'Number.float',
                    'StringValue': str(latitude)
                },
                'longitude': {
                    'DataType': 'Number.float',
                    'StringValue': str(longitude)
                },
                'heart_rate': {
                    'DataType': 'Number',
                    'StringValue': str(heart_rate)
        }
            },
            MessageBody=(
                'test body'
            )
        )

        print(response['MessageId'])

        time.sleep(PERIOD)


def get_position(origin):
    return


def get_frequency(avg_freq):
    return
