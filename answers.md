Your answers to the questions go here.
### Setup the environment

>Answer: I am using macOS Sierra Version 10.12.6 for this Challenge. I installed and set up Vagrant with VirtualBox as provider.

### Collecting Metrics

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
>Answer: [Sign up here](https://www.datadoghq.com/#), get a datadog account for free for 14 days.

>login, click on [_integration-Agent_](https://app.datadoghq.com/account/settings#agent/mac) in DataDog on the left column and follow the installation instructions for Mac OS X to install the Agent.
> The datadog can be installed on OS X easily as:

```
DD_API_KEY=63ab065b2982aed65fff538ba18a93ba bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

>Answer: Change direction by type _cd ~/.datadog-agent_ in terminal, then type _vim datadog.conf_ to open and edit the configuration file.

[reference](https://docs.datadoghq.com/guides/tagging/)

<img src="https://github.com/zhang587/datadog_screenshots/blob/master/add_tags.png" />

After a few minutes refresh the Datadog, go to [_Infrastructure - Host Map_], the tags are now shown in there.

<img src="https://github.com/zhang587/datadog_screenshots/blob/master/tag_host_map.png" />

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

>Answer: I am using PostgresSQL for this part, for how to download and install the software PostgresSQL please refer to -> [Download PostgresSQL here](https://www.postgresql.org/download/macosx/)

I used MySQL at first, but ran into some issues during validation process. I could have solve the issue, but it'll take lots of time, so I changed to PostgresSQL instead.

>Find the PostgresSQL API under [_Integrations-Integrations_](https://app.datadoghq.com/account/settings), click _install_, then click on _Configuration_ tab.

<img src="https://github.com/zhang587/datadog_screenshots/blob/master/integration.png" />

>Create a read-only datadog user with proper access to the PostgresSQL Server.

```
create user datadog with password 'password_for_datadog';

grant SELECT ON pg_stat_database to datadog;

```

>Configure the Agent to connect to the PostgreSQL server

>Restart the Agent

>Type _datadog-agent info_ in Terminal to check states.


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

>Answer:

Here is `my_metric.py`:

```

from random import randint

from checks import AgentCheck

 class HelloCheck(AgentCheck):

    def check(self, instance):

        self.gauge('my_metric', randint(1,1000))

```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

>Answer: I did this by editing the `my_metric.yaml` file so that it specifies the collection interval:

```
init_config:
 instances:
    -   min_collection_interval: 45
```
If `min_collection_interval` is not specified, the check would run about every 15-20 seconds.

*Bonus Question: Can you change the collection interval without modifying the Python check file you created?

>Answer: Yes, the collection interval can be changed by changing the `min_collection_interval` in the `.yaml` configuration file.


### Visualizing Data

* Utilize the Datadog API to create a Timeboard

> Answer: I wrote a python script (attached as 'timeboard.py') to use the Datadog API to create a Timeboard.

* Bonus Question: What is the Anomaly graph displaying?

> Answer: The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database were growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert.

### Monitoring Data

> Answer:

  Screenshot of timeboard: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/timeboard.png" />

  Screenshot of email: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/email.png" />

*  Bonus Question: Scheduled downtime

> Answer:

  Downtime hat silences it from 7pm to 9am daily on M-F: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/downtime_daily.png" />

  Downtime hat silences it silences it all day on Sat-Sun: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/downtime_weekend.png" />

  Screenshot of email: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/email_notification.png" />

### Level 4 - Collecting APM Data

>Answer: The instrumented Flask app is included as `flask_apm_app.py`.

Dashboard screenshot: <img src="https://github.com/zhang587/datadog_screenshots/blob/master/dashboard.png" />

APM screenshot: <img src="https://github.com/zhang587/datadog_screenshots/blob/master/APM.png" />


* What is the difference between a Service and a Resource?
A service is a set of processes that all do the same job. For instance, a web application could consist of a webapp service and a database service. A resource is a particular action for a given service.


### Final Question: Is there anything creative you would use Datadog for?
I like working out and being fit, and I think it would be very interesting to have Datadog to visualize various factors that might affect a person's fitness journey. Factors include:

-number of hours spent in the gym
-number of calories input
-metabolic rate
-magnesium intake
-vitamin D intake
-alcohol intake
-social media usage

It would be interesting to see those kinds of data display in the Datadog dashboard over years, and monitor changes in each factor, therefore people can have better sense of getting fit and healthy.

### Below are the scripts attached, 'timeboard.py' and 'flask_apm_app.py'

# timeboard.py
```
from datadog import initialize, api

options = {"api_key": "76e7696c9a143d8f5111365fa4e61d26", "app_key":"21e7378eff399c099bc5da859a21df54962ac0a6" }
initialize(**options)
title = "Shay's Timeboard"
description = "Tracks my_metric"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over time"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.database_size{role:database:mongodb}, 'basic', 3)"
             }],
        "viz": "timeseries"
    },
    "title": "Database size anomalies"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Hourly Rollup Sum of my_metric"
}]

template_variables = [{
    "name": "i-0a9ff2c19f22d237a",
    "prefix": "host",
    "default": "host:i-0a9ff2c19f22d237a"
}]

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

# flask_apm_app.py

```
import logging
import sys
import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from flask import Flask

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
 
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```
