from event_gen.EventGenerator import EventGenerator


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
