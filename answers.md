Your answers to the questions go here.
Section A :  Collecting Metrics
Q.1) Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Ans - https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/Img1.PNG

Q.2) Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Ans - https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/Install_database_integration.PNG

Q.3) Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Ans - ```python:checks.d/myMetric.py
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck
# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"
class myMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randrange(1000))
``

Q.4) Change your check's collection interval so that it only submits the metric once every 45 seconds.
Ans - ``` checks.d/myMetric.yaml
init_config:
　　min_collection_interval: 45
instances: [{}]

Q.5) Bonus Question Can you change the collection interval without modifying the Python check file you created?
Ans - May be there is an API for that.
