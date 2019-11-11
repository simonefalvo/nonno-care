from threading import Thread
import time
from random import random, seed
from wirlband_simulator.sqs import send_message


class AsynchronousSOSEventThread(Thread):

    seed = None

    def __init__(self, user):
        self.my_user = user
        self.max_sleep = 60  # TODO: rendere parametri
        self.min_sleep = 0
        Thread.__init__(self)

    def run(self):

        print("Thread SOS avviato")
        while True:
            sleep_time = self.min_sleep + (random() * (self.max_sleep - self.min_sleep))
            time.sleep(sleep_time)

            print("Thread SOS risvegliato dopo sleep di ", sleep_time)

            # genero evento asincrono
            send_message(self.my_user, sos=1)

            print("Thread ha inoltrato l'evento SOS ")
