import sys
import boto3
import time
import random
import math

from User import User
from event_gen.EventGenerator import EventGenerator
from event_gen.ActivityEventGenerator import ActivityEventGenerator
from event_gen.SosEventGenerator import SosEventGenerator
from EventSenderThread import EventSenderThread

import aws.cloudformation as cf
import aws.sqs as sqs

STACK_NAME = "nonno-stack"

SAMPLE_PERIOD = 120  # Sample period
#AVG_FALL_PERIOD = 2 * 60 * 60  # seconds
#AVG_ACTIVITY_PERIOD = 1 * 60 * 60  # seconds
#AVG_SOS_PERIOD = 1 * 15 * 24 * 3600  # seconds (twice a month)
AVG_FALL_PERIOD = 120  # seconds
AVG_SOS_PERIOD = 120  # seconds
AVG_ACTIVITY_PERIOD = 120  # seconds

K = 1  # time compression


def main():

    sensor_id = sys.argv[1]
    processes_number = int(sys.argv[2])

    # random start
    start_delay = random.uniform(0, math.log2(processes_number))
    time.sleep(start_delay)

    # register new user
    user = User(sensor_id, "Pumero", "nonnocare.notify@gmail.com")
    register_user(user)

    queue_url = cf.stack_output(STACK_NAME, "SQSQueue")

    periodic_event_gen = EventGenerator(user)
    sos_event_gen = SosEventGenerator(user)
    activity_event_gen = ActivityEventGenerator(user, "./wirlband_simulator/event_gen/activities")
    fall_event_gen = ActivityEventGenerator(user, "./wirlband_simulator/event_gen/falls")

    EventSenderThread(sos_event_gen, AVG_SOS_PERIOD, queue_url).start()
    EventSenderThread(activity_event_gen, AVG_ACTIVITY_PERIOD, queue_url).start()
    EventSenderThread(fall_event_gen, AVG_FALL_PERIOD, queue_url).start()

    while True:
        user.next_position(SAMPLE_PERIOD)
        pe = periodic_event_gen.next()
        sqs.send_message(queue_url, pe)
        print("Periodic event user {}".format(user.sensor_id))
        time.sleep(K * SAMPLE_PERIOD)


def register_user(user):
    table_name = cf.stack_output(STACK_NAME, "UserDataTable")
    # Store user data
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table.put_item(
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


if __name__ == '__main__':
    main()
