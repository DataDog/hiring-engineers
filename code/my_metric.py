# Jason Jakary, Datadog SE Candidate
# September 2021
# Agent Check to generate random integer between 0-1000
# Files this script is reliant on:
#   /etc/datadog-agent/conf.d/my_metric.yaml

# Import the "random" module to get the tool to creat random numbers
import random

# Import the "AgentCheck" module to allow us to use the AgentCheck Class
try:
   # Assume the agent is up to date
   from datadog_checks.base import AgentCheck
except ImportError:
  # If the agent is older than 6.6.0, get AgentCheck form the old module
  from checks import Agent Check
  
# Define this to be the first version of my_metric
__version__="1.0!

# Use the class to create the guage variable "my_metric" and assign a random integer between 0-1000 to its value
class NumberGen(AgentCheck):
    def check(self, instance):
        self.gauge("my_metric", random.randint(0,1000), tags=["metric_sumbission_type:gauge"])
