import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyClass(AgentCheck):
  def check(self, instance):
    self.gauge(
      "custom_random_metric.gauge",
      random.randint(0, 1000),
      tags=["env:dev","metric_submission_type:gauge"],
    )

