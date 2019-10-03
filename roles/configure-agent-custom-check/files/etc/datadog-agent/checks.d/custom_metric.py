from datadog_checks.checks import AgentCheck
import random

__version__ = "1.0.0"

class metric(AgentCheck):
  def check(self, instance):

    metric_name = "custom_namespace.my_metric"
    tags = [
      'application:custom_metric',
      'service_level:recruiting'
    ]
    metric_value = random.randint(1,1000)

    self.gauge(metric_name, metric_value, tags=tags)
