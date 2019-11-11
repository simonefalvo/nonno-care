from threading import Thread
import time
from random import random, seed
from wirlband_simulator.FallEvent import FallEvent
from wirlband_simulator.sqs import send_message


class AsynchronousFallEventThread(Thread):

    seed = None

    def __init__(self, user):
        self.my_user = user
        self.fall_event_generator = FallEvent()
        self.max_sleep = 60  # TODO: rendere parametri
        self.min_sleep = 0
        Thread.__init__(self)

    def run(self):

        print("Thread Caduta avviato")
        while True:
            sleep_time = self.min_sleep + (random() * (self.max_sleep - self.min_sleep))
            time.sleep(sleep_time)

            print("Thread Caduta risvegliato dopo sleep di ", sleep_time)

            # genero evento asincrono
            fall_event = self.fall_event_generator.generate_and_get_event()
            send_message(self.my_user, fall_event)

            print("Thread Caduta ha inoltrato l'evento: ", self.fall_event_generator.get_event_name())

            # TODO: controllare che evento sia stato di caduta
            # dopo la caduta con una certa p mando sos
            sleep_time = self.min_sleep + (random() * (self.max_sleep - self.min_sleep))
            time.sleep(sleep_time)
            if random() > 0.5:
                send_message(self.my_user, fall_data=None, sos=1)
                print("Thread Caduta ha inoltrato SOS")
