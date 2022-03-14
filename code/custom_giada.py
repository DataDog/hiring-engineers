## Custom Agent Check for the hiring exercise
#  It submits a metric called "giada_custom.metric"
#  with a random value between 0 and 1000.

import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyClass(AgentCheck):
    def check(self, instance):
        self.gauge(
                "giada_custom.metric",
                random.randint(0, 1000),
                tags=["custom_metric:yes","metric_submission_type:gauge"],
                )