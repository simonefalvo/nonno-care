import os
from random import seed, random


# rendere classe statica?


class FallEvent:

    def __init__(self):
        self.files = []
        self.event_file_name = ""
        self.event = ""
        self.__list_file_fall()
        self.generate_event()

    # privato
    def __list_file_fall(self):
        path = "wirlband_simulator/fall_file/"
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.csv' in file:
                    self.files.append(os.path.join(r, file))

    # privato
    def __fall_data(self):
        with open(self.event_file_name) as f:
            self.event = f.read() + '\n'

    def generate_event(self):
        i = round(random() * (len(self.files) - 1))
        self.event_file_name = self.files[i]
        self.__fall_data()

    def get_event_name(self):
        return self.event_file_name

    def get_event(self):
        return self.event

    def generate_and_get_event(self):
        self.generate_event()
        return self.get_event()
