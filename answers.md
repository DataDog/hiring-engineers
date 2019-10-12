Your answers to the questions go here.

#Prerequisites: I created a Linux vm using Vagrant.

Screenshot: https://drive.google.com/file/d/1ZnBlCl1T9MLoPDDv-FG-N1hDcsxjP5xz/view?usp=sharing

I installed the Datadog Linux Agent: https://drive.google.com/file/d/1xhHh5jPgOVETmjkXa77hwAPKvLWEnOuY/view?usp=sharing

I installed MySQL and the Datadog Integration for MySQL: https://drive.google.com/file/d/1WmQUJlqU4CoWPsqNBwvpXdavA5qFqtYW/view?usp=sharing

#Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000
#This is my code:

try:

from checks import AgentCheck

except ImportError:

from datadog_checks.checks import AgentCheck

class MyMetric(MyMetric):

def check(self, instance):

self.gauge('my.metric', 1, tags=['role:database'])

#Change your check's collection interval so that it only submits the metric once every 45 seconds.
#This is my code

init_config:

instances:
  - min_collection_interval: 45
