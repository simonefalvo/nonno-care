from event_gen.EventGenerator import EventGenerator
from User import User


class SosEventGenerator(EventGenerator):

    def next(self):
        event = self.build_event()
        event['sos'] = {
            'DataType': 'String',
            'StringValue': '1'
        }
        return event

    def description(self):
        return "SOS event"


if __name__ == '__main__':
    sample_user = User(1, "test_user", "test@email.com")
    eg = SosEventGenerator(sample_user)
    print(eg.next())
