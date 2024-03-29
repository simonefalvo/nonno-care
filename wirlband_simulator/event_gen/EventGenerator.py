import time


class EventGenerator:

    def __init__(self, user):
        self.__user = user

    @property
    def user(self):
        return self.__user

    def build_event(self):
        timestamp = time.time()
        event = {
            'sensor_id': {
                'DataType': 'Number',
                'StringValue': str(self.user.sensor_id)
            },
            'timestamp': {
                'DataType': 'String',
                'StringValue': str(timestamp)
            },
            'latitude': {
                'DataType': 'Number.float',
                'StringValue': str(self.user.current_latitude)
            },
            'longitude': {
                'DataType': 'Number.float',
                'StringValue': str(self.user.current_longitude)
            },
            'heart_rate': {
                'DataType': 'Number',
                'StringValue': str(self.user.current_hrate())
            }
        }
        return event

    def next(self):
        return self.build_event()
