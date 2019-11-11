import boto3
import time
from wirlband_simulator.User import User
from wirlband_simulator import AsynchronousSOSEventThread
from wirlband_simulator import AsynchronousFallEventThread
from wirlband_simulator.sqs import send_message


PERIOD = 120  # Sample period
QUEUE_URL = "https://sqs.eu-west-3.amazonaws.com/043090642581/nonno-stack-SQSQueue-1LBSEA3CRURF6"
USER_DATA_TABLE = "nonno-stack-UserDataTable-125JIRLB2B5XP"


def main():

    sensor_id = 4
    user = User(sensor_id, "Pumero", "pietrangeli.aldo@gmail.com")
    register_user(user)

    fall_event_simulator = AsynchronousFallEventThread.AsynchronousFallEventThread(user)
    sos_event_simulator = AsynchronousSOSEventThread.AsynchronousSOSEventThread(user)
    fall_event_simulator.start()
    sos_event_simulator.start()

    counter = 0
    try:
        while True:
            counter += 1
            user.next_position(PERIOD)
            send_message(user)
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        fall_event_simulator.join()
        sos_event_simulator.join()
        exit()
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


if __name__ == '__main__':
    main()
