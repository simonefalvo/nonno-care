from threading import Thread
import time
import numpy as np
from sqs import send_message


class AsynchronousSOSEventThread(Thread):

    def __init__(self, user, avg_period):
        self.my_user = user
        self.avg_period = avg_period
        Thread.__init__(self)

    def run(self):

        print("Thread SOS avviato")
        while True:
            sleep_time = np.random.exponential(scale=self.avg_period)
            time.sleep(sleep_time)
            print("Thread SOS risvegliato dopo sleep di ", sleep_time)

            # genero evento asincrono
            send_message(self.my_user, sos=1)

            print("Thread ha inoltrato l'evento SOS ")
