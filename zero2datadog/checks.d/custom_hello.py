import random
from datadog_checks.base import AgentCheck # This project uses Agent >6.6.0

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "0.1.0"

"""Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

    Thank you, https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
"""
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge(
            "my_metric",
            random.randint(0, 1000),
            tags=["env:dev",
                  "admin_email:jitkelme@gmail.com",
                  "metric_submission_type:gauge"],
        )

