Your answers to the questions go here.

# Collecting Metrics:

**Q1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![A1](https://github.com/jhhys/hiring-engineers/blob/master/Add%20tags%20in%20the%20Agent%20config%20file%20.png)

**Q2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![A2](https://github.com/jhhys/hiring-engineers/blob/master/Install%20a%20database%20on%20your%20machine.png)

**Q3.Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

A. checks.d/myMetric.py
```
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
```

**Q4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

A. conf.d/myMetric.yaml

``` 
init_config:
　　min_collection_interval: 45

instances: [{}]

```

**Q5.Bonus Question Can you change the collection interval without modifying the Python check file you created?
A. I could not find the answer. Maybe there is a API for that?

# Visualizing Data:

**Q6. Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

![A](https://github.com/jhhys/hiring-engineers/blob/master/Timeboard.png)

**Q7. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

A. myTimeboard.py
```
from datadog import initialize, api

options = {
    'api_key': 'ea79ad28beeb99688cb324fc897d8d64',
    'app_key': 'bee880364a846ba5e75c86b4fdf10c9435052854'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."

graphs = [
{
    "definition": {
        "events": [],
        "requests": [{"q": "avg:my_metric{admin:harry,host:training.localdomain}"}],
        "viz": "timeseries"
    },
    "title": "custom metric scoped over your host"
},
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:mysql.innodb.buffer_pool_free{*}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Any metric from the Integration on your Database with the anomaly function applied"
},
{
    "definition": {
        "events": [],
        "requests": [{"q": "avg:my_metric{admin:harry,host:training.localdomain}.rollup(sum,3600)"}],
        "viz": "timeseries"
    },
    "title": "Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket"
}
]


template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
#                     template_variables=template_variables,
                     read_only=read_only)

```

**Q8. Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

A. I could not find thw way to change the timeframe to the value less than 1 hour.

**Q9.Bonus Question: What is the Anomaly graph displaying?

A. It shows parts in a charts in where some graphs are show different movement.






Q. Bonus Question: What is the difference between a Service and a Resource?
A. A service is an entry point of an application and a resource is a particular action for a given service.

Q. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
https://app.datadoghq.com/apm/service/flask/flask.request?end=1542681849016&env=prod&paused=false&start=1542678249016

Q. Is there anything creative you would use Datadog for?
A. Availability of devices used for IoT


