import boto3
import time
from wirlband_simulator.User import User
from wirlband_simulator import AsynchronousEventThread


PERIOD = 120  # Sample period
QUEUE_URL = "https://sqs.eu-west-3.amazonaws.com/043090642581/nonno-stack-SQSQueue-1INIID3URVE6W"
USER_DATA_TABLE = "nonno-stack-UserDataTable-PUC8NHYXVQCO"


def main():

    sensor_id = 4
    user = User(sensor_id, "Pumero", "pietrangeli.aldo@gmail.com")
    register_user(user)

    fall_event_simulator = AsynchronousEventThread.AsynchronusEventThread(user)
    fall_event_simulator.start()

    counter = 0
    try:
        while True:
            counter += 1
            user.next_position()
            send_message(user)
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        fall_event_simulator.join()
        pass


def register_user(user):
    # Store user data
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(USER_DATA_TABLE)
    response = table.put_item(
        Item={
            'sensor_id': str(user.sensor_id),
            'safety_latitude': str(user.safety_latitude),
            'safety_longitude': str(user.safety_longitude),
            'avg_hrate': str(user.avg_hrate),
            'var_hrate': str(user.var_hrate),
            'email': user.email
        }
    )
    print(response)


def send_message(user, fall=None):

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

    if fall is not None:
        attributes['fall'] = {
                'DataType': 'String',
                'StringValue': fall
            }

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageAttributes=attributes,
        MessageBody=(
            'simulated event'
        )
    )

    print(response['MessageId'])


if __name__ == '__main__':
    main()
