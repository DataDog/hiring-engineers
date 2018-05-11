import random

from checks import AgentCheck


class CustomCheck(AgentCheck):
    def check(self, instance):
        my_metric_value = random.randint(0, 1000)
        self.gauge('my_metric', my_metric_value)


if __name__ == '__main__':
    check.check(instance)
