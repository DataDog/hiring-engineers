import random
import time

from checks import AgentCheck


def __main__():
    RandomGauge().check()


class RandomGauge(AgentCheck):

    def check(self, instance):
        value = random.random()
        payload = {
            'timestamp': int(time.time()),
            'event_type': 'random_event',
            'api_key': '9250414dc14ae45453222f2334bcb7e6',
            'msg_title': 'Random event',
            'msg_text': 'New random event',
            'aggregation_key': 'events',
        }

        self.log.info('Random value sent')
        self.event(payload)
        self.gauge('test.support.random', value)


if __name__ == '__main__':
    __main__()
