# By Roger Berlind

# project
from config import _is_affirmative
from checks import AgentCheck
from util import Platform

# stdlib
import random

# Load values from the check config file
first = self.init_config.get('first', 1)
last = self.init_config.get('last', 100)

class MyRandomValueCheck(AgentCheck):
    def check(self, instance):
        # Load values from the randomvalue.yaml file
        first = self.init_config.get('first', 1)
        last = self.init_config.get('last', 100)

        # Generate the random value and log that we did it
        self.gauge('random.value', random.randint(first, last))
        self.log.info("Just set a gauge to a random integer between the first and last values in the check configuration file.")
