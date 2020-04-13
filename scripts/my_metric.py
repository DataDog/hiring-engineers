import random

from datadog_checks.base import AgentCheck
from checks import AgentCheck

class MyMetric(AgentCheck):
  def check(self, instance):
    self.count( "my_metric.count", 2, tags=["env:dev","metric_submission_type:count"])
    self.count( "my_metric.decrement", -1, tags=["env:dev","metric_submission_type:count"])
    self.count( "my_metric.increment", 1, tags=["env:dev","metric_submission_type:count"])
    self.rate( "my_metric.rate", 1, tags=["env:dev","metric_submission_type:rate"])
    self.gauge('my_metric.gauge', random.randrange(1000), tags=["env:dev","metric_submission_type:gauge"])
    self.monotonic_count( "my_metric.monotonic_count", 2, tags=["env:dev","metric_submission_type:monotonic_count"])

    # Calling the functions below twice simulates several metrics submissions during one Agent run:
    self.histogram( "my_metric.histogram", random.randrange(1000), tags=["env:dev","metric_submission_type:histogram"])
    self.histogram( "my_metric.histogram", random.randrange(1000), tags=["env:dev","metric_submission_type:histogram"])

