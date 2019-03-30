Your answers to the questions go here.

I Collecting Metrics:

1.- Tagging
tags: role:db, env:pre, roletype:mysql5.7

2.- Installed Mysql v. 5.7

mysql-client-5.7				install
mysql-client-core-5.7				install
mysql-common					install
mysql-server					install
mysql-server-5.7				install
mysql-server-core-5.7				install

3.- Create Agent Check

Check file:
---------

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


class MyCheck(AgentCheck):
    def check(self, instance):
        value = random.randint(0,1001)
        self.gauge('my_metric', value)
-------
Check conf file:

init_config:

instances:
  - min_collection_interval: 45
-------

II Visualizing Data:

1.- Create a Dashboar via API
Created with a python client script
2.- Taken an screenshot of the my_metric graph

Bonus question
I had to add the anomaly function to the first timeseries showing the my_metric, because the mysql metrics were mostly flat. 

So, the graph with the anomaly function highlights in red the values that are not expected (too low/high) based on the values seen in the past. In grey the graph shows the predicted values based on the algorithm used for the anomaly function.


III Monitoring Data:

Instrument flask app  (python based, flask_app.py)

- Activated tracing datadog agent config file
- install library sudo pip3 install ddtrace
- run ddtrace-run python3 flask_app.py 

Also, provided a simulator of activity to generate traffic to the app

Screenboard url
https://p.datadoghq.com/sb/9d4bnv9ca849v6du-f5d7594f12c27f8853f72dc5d4ecccb1

Bonus Question: What is the difference between a Service and a Resource?
A service is process that accepts requests, and do some function. They are develop in languages like java, php, python, go, etc. Resources are the different requests of a service, in a web app is an endpoint. In our instrumented application, flask is the service (a process that accepts web requests from a browser), and the web requests /, /api/apm, etc are the resources.

Final Question

I would suggest this idea:

Monitor IOT devices, in particular smart trucks, for fleet management. Datadog agent could collect data from the truck itself (like temperature, location, fuel level, tires pressure, hours driving, etc) and complement services like the ones envisioned in the following article:

http://www.supplychain247.com/article/how_the_internet_of_things_transforms_trucking

Datadog dashboards could provide all this information with sexy reports,  tons of options to combine different indicators, and more importantly, alerts could enforce logistics and regulation in place (like drivers cannot drive more than x hours, or the need to check the tires pressure because is too low). With the inherent multy-tenancy of datadog Saas environment, this scheme could be replicated for different customers very easily.





