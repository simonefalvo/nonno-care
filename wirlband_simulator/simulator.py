import boto3
import time
import random


PERIOD = 120  # Sample period
AVG_HRATE = 75
VAR_HRATE = 15

QUEUE_URL = "https://sqs.eu-west-3.amazonaws.com/043090642581/nonno-stack-SQSQueue-1IFL6A226TIJK"
USER_DATA_TABLE = "nonno-stack-UserDataTable-57S7JPDYJ74C"


def main():

    sensor_id = 4
    register_user(sensor_id)

    counter = 0
    while True:
        counter += 1
        latitude = 41.858362
        longitude = 12.635893
        heart_rate = 106

        send_message(sensor_id, latitude, longitude, heart_rate)
        print("Sent messages: ", counter)

        time.sleep(PERIOD)


def register_user(sensor_id):

    # Generate user data
    avg_hrate = int(random.gauss(AVG_HRATE, VAR_HRATE))
    var_hrate = VAR_HRATE
    safety_latitude = random.uniform(-90, 90)
    safety_longitude = random.uniform(-180, 180)
    # safety_radius = random.uniform(10, 15)

    # Store user data
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(USER_DATA_TABLE)
    response = table.put_item(
        Item={
            'sensor_id': str(sensor_id),
            'safety_latitude': str(safety_latitude),
            'safety_longitude': str(safety_longitude),
            'avg_hrate': str(avg_hrate),
            'var_hrate': str(var_hrate)
        }
    )
    print(response)


def send_message(sensor_id, latitude, longitude, heart_rate):

    timestamp = time.time()

    # Create SQS client
    sqs = boto3.client('sqs')

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
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


def get_position(origin):
    return


def get_frequency(avg_hrate):
    return


if __name__ == '__main__':
    main()
