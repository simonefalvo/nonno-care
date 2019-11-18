import os
import random

from event_gen.EventGenerator import EventGenerator
from User import User


class ActivityEventGenerator(EventGenerator):

    def __init__(self, user, data_path):
        self.__user = user
        self.__data_path = data_path
        self.__activity_file = ""
        self.__data_files = []
        self.__populate_data_files()

    @property
    def user(self):
        return self.__user

    @property
    def data_path(self):
        return self.__data_path

    @property
    def data_files(self):
        return self.__data_files

    @property
    def activity_file(self):
        return self.__activity_file

    @activity_file.setter
    def activity_file(self, file):
        self.__activity_file = file

    def __populate_data_files(self):
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.data_path):
            for file in f:
                if '.csv' in file:
                    self.data_files.append(os.path.join(r, file))

    def next(self):
        i = round(random.random() * (len(self.data_files) - 1))
        self.activity_file = self.data_files[i]
        # open and read file
        with open(self.activity_file) as f:
            activity_data = f.read() + '\n'
        event = self.build_event()
        event['fall_data'] = {
                'DataType': 'String',
                'StringValue': activity_data
        }
        return event

    def description(self):
        return self.activity_file


if __name__ == '__main__':
    sample_user = User(1, "test_user", "test@email.com")
    eg = ActivityEventGenerator(sample_user, "./fall_file")
    print(eg.next())
    print("file name: {}".format(eg.activity_file))
