import sys
import boto3
import time

from User import User
import AsynchronousSOSEventThread
import AsynchronousFallEventThread
from sqs import send_message


USER_DATA_TABLE = "nonno-stack-UserDataTable-IACOAI88802V"

SAMPLE_PERIOD = 120  # Sample period
#FALL_PERIOD = 1 * 60 * 60  # seconds
#SOS_PERIOD = 1 * 24 * 3600  # seconds
AVG_FALL_PERIOD = 120  # seconds
AVG_SOS_PERIOD = 120  # seconds

K = 1  # time compression


def main():

    sensor_id = sys.argv[1]
    user = User(sensor_id, "Pumero", "nonnocare.notify@gmail.com")
    register_user(user)

    fall_event_simulator = AsynchronousFallEventThread.AsynchronousFallEventThread(user, K * AVG_FALL_PERIOD)
    sos_event_simulator = AsynchronousSOSEventThread.AsynchronousSOSEventThread(user, K * AVG_SOS_PERIOD)
    fall_event_simulator.start()
    sos_event_simulator.start()

    counter = 0
    try:
        while True:
            counter += 1
            user.next_position(SAMPLE_PERIOD)
            send_message(user)
            time.sleep(K * SAMPLE_PERIOD)
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
            'safety_radius': str(user.safety_radius),
            'avg_hrate': str(user.avg_hrate),
            'var_hrate': str(user.var_hrate),
            'email': user.email
        }
    )
    print(response)


if __name__ == '__main__':
    main()
