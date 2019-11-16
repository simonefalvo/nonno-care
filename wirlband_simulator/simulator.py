import sys
import os
import boto3
import time
import random
import math

from User import User
import AsynchronousSOSEventThread as sos_thread
import AsynchronousFallEventThread as fall_thread
from sqs import send_message

import aws.cloudformation as cf

STACK_NAME = "nonno-stack"

SAMPLE_PERIOD = 120  # Sample period
#FALL_PERIOD = 1 * 60 * 60  # seconds
#SOS_PERIOD = 1 * 24 * 3600  # seconds
AVG_FALL_PERIOD = 120  # seconds
AVG_SOS_PERIOD = 120  # seconds

K = 1  # time compression


def main():
    print(os.getcwd())
    sensor_id = sys.argv[1]
    processes_number = int(sys.argv[2])
    # random start
    start_delay = random.uniform(0, math.log2(processes_number))
    time.sleep(start_delay)

    user = User(sensor_id, "Pumero", "nonnocare.notify@gmail.com")
    register_user(user)

    queue_url = cf.stack_output(STACK_NAME, "SQSQueue")

    fall_event_simulator = fall_thread.AsynchronousFallEventThread(user, queue_url, K * AVG_FALL_PERIOD)
    sos_event_simulator = sos_thread.AsynchronousSOSEventThread(user, queue_url, K * AVG_SOS_PERIOD)
    fall_event_simulator.start()
    sos_event_simulator.start()

    counter = 0
    try:
        while True:
            counter += 1
            user.next_position(SAMPLE_PERIOD)
            send_message(user, queue_url)
            time.sleep(K * SAMPLE_PERIOD)
    except KeyboardInterrupt:
        fall_event_simulator.join()
        sos_event_simulator.join()
        exit()
        pass


def register_user(user):
    table_name = cf.stack_output(STACK_NAME, "UserDataTable")
    # Store user data
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
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
