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



Section B : Visualizing Data
Q.1) Utilize the Datadog API to create a Timeboard that contains:

    Your custom metric scoped over your host.
    Any metric from the Integration on your Database with the anomaly function applied.
    Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Ans - myTimeboard.py (https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/myTimeboard.py)

Q.2) Set the Timeboard's timeframe to the past 5 minutes.Take a snapshot of this graph and use the @ notation to send it to yourself.
Ans - I couldn't find a way to do it below 1 hour.

Q.3) What is the Anomaly graph displaying?
Ans - It shows parts in a chart where some of the graphs are showing different movement.





Section C : Monitoring Data
Q.1) Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Ans -  https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/Alert_JSON.PNG
       https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/Warning_JSON.PNG
       
Q.2) Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
Ans - Downtime1(https://github.com/sshinde16/hiring-engineers/blob/SurabhiShinde_Solutions_Engineer/Downtime1.PNG)
      Downtime2(
