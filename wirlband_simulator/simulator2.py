import sys
import time
import random
from threading import Thread

# IDE imports
#from wirlband_simulator.User import User
#from wirlband_simulator.event_gen.EventGenerator import EventGenerator
#from wirlband_simulator.event_gen.ActivityEventGenerator import ActivityEventGenerator
#from wirlband_simulator.event_gen.SosEventGenerator import SosEventGenerator
#from wirlband_simulator.EventSenderThread import EventSenderThread
#
#import wirlband_simulator.aws.cloudformation as cf
#import wirlband_simulator.aws.dynamodb as dynamodb
#import wirlband_simulator.aws.sqs as sqs

from User import User
from event_gen.EventGenerator import EventGenerator
from event_gen.ActivityEventGenerator import ActivityEventGenerator
from event_gen.SosEventGenerator import SosEventGenerator
from EventSenderThread import EventSenderThread

import aws.cloudformation as cf
import aws.dynamodb as dynamodb
import aws.sqs as sqs

STACK_NAME = "nonno-stack"

SAMPLE_PERIOD = 10 * 60  # Sample period
AVG_FALL_PERIOD = 1 * 30 * 24 * 60 * 60  # seconds (once a month)
AVG_ACTIVITY_PERIOD = 3/2 * 1 * 60 * 60  # seconds (16 events in a 24 hours)
AVG_SOS_PERIOD = 1 * 15 * 24 * 3600  # seconds (twice a month)
# AVG_FALL_PERIOD = 120  # seconds
# AVG_SOS_PERIOD = 120  # seconds
# AVG_ACTIVITY_PERIOD = 120  # seconds

K = 1/32  # time compression


class UserThread(Thread):

    def __init__(self, sensor_id):
        Thread.__init__(self)
        self.__sensor_id = sensor_id

    @property
    def sensor_id(self):
        return self.__sensor_id

    def run(self):
        # random start
        start_delay = random.uniform(0, max(0.0, K * SAMPLE_PERIOD))
        time.sleep(start_delay)

        # register new user
        user = User(self.sensor_id, "Pumero", "nonnocare.notify@gmail.com")
        register_user(user)

        queue_url = cf.stack_output(STACK_NAME, "SQSQueue")
        #queue_url = "https://sqs.eu-west-3.amazonaws.com/043090642581/nonno-stack-SQSQueue-976QBGKN1KC9"
        periodic_event_gen = EventGenerator(user)
        sos_event_gen = SosEventGenerator(user)
        activity_event_gen = ActivityEventGenerator(user, "./event_gen/activities")
        fall_event_gen = ActivityEventGenerator(user, "./event_gen/falls")

        EventSenderThread(sos_event_gen, K * AVG_SOS_PERIOD, queue_url).start()
        EventSenderThread(activity_event_gen, K * AVG_ACTIVITY_PERIOD, queue_url).start()
        EventSenderThread(fall_event_gen, K * AVG_FALL_PERIOD, queue_url).start()

        while True:
            user.next_position(SAMPLE_PERIOD)
            pe = periodic_event_gen.next()
            sqs.send_message(queue_url, pe)
            print("{}: Periodic event".format(user.sensor_id))
            time.sleep(K * SAMPLE_PERIOD)


def register_user(user):
    table_name = cf.stack_output(STACK_NAME, "UserDataTable")
    #table_name = "nonno-stack-UserDataTable-13JTNWIVLYER5"
    # Store user data
    return dynamodb.put_item(table_name=table_name,
                             item={
                                 'sensor_id': str(user.sensor_id),
                                 'safety_latitude': str(user.safety_latitude),
                                 'safety_longitude': str(user.safety_longitude),
                                 'safety_radius': str(user.safety_radius),
                                 'avg_hrate': str(user.avg_hrate),
                                 'var_hrate': str(user.var_hrate),
                                 'email': user.email
                             }
                             )


def main():
    sensors_number = int(sys.argv[1])
    for sensor_id in range(1, sensors_number + 1):
        UserThread(sensor_id).start()


if __name__ == '__main__':
    main()
