from threading import Thread
import time
import numpy as np

import aws.sqs as sqs


class EventSenderThread(Thread):

    def __init__(self, event_generator, avg_period, sqs_connection, queue_url):
        Thread.__init__(self)
        self.__event_generator = event_generator
        self.__avg_period = avg_period
        self.__queue_url = queue_url
        self.__sqs = sqs_connection

    @property
    def event_generator(self):
        return self.__event_generator

    @property
    def avg_period(self):
        return self.__avg_period

    @property
    def queue_url(self):
        return self.__queue_url

    @property
    def sqs(self):
        return self.__sqs

    def run(self):
        while True:
            sleep_time = np.random.exponential(scale=self.avg_period)
            time.sleep(sleep_time)

            event = self.event_generator.next()
            sqs.send_message(self.sqs, self.queue_url, event)
            print("{}: {}".format(self.event_generator.user.sensor_id, self.event_generator.description()))
