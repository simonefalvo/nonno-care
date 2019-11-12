import sys
import boto3
import time
from wirlband_simulator.User import User
from wirlband_simulator import AsynchronousSOSEventThread
from wirlband_simulator import AsynchronousFallEventThread
from wirlband_simulator.sqs import send_message


USER_DATA_TABLE = "nonno-stack-UserDataTable-125JIRLB2B5XP"

SAMPLE_PERIOD = 120  # Sample period
#FALL_PERIOD = 1 * 60 * 60  # seconds
#SOS_PERIOD = 1 * 24 * 3600  # seconds
AVG_FALL_PERIOD = 120  # seconds
AVG_SOS_PERIOD = 120  # seconds

def main():

    sensor_id = sys.argv[1]
    user = User(sensor_id, "Pumero", "pietrangeli.aldo@gmail.com")
    register_user(user)

    fall_event_simulator = AsynchronousFallEventThread.AsynchronousFallEventThread(user, AVG_FALL_PERIOD)
    sos_event_simulator = AsynchronousSOSEventThread.AsynchronousSOSEventThread(user, AVG_SOS_PERIOD)
    fall_event_simulator.start()
    sos_event_simulator.start()

    counter = 0
    try:
        while True:
            counter += 1
            user.next_position(SAMPLE_PERIOD)
            send_message(user)
            time.sleep(SAMPLE_PERIOD)
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
