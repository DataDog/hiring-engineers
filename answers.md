# Prerequisites - Setup the environment

- Install vagrant and Virtualbox on Mac 
- Start Vagrant with Ubuntu v. 16.04
```
vagrant init ubuntu/xenial64
vagrant up
vagrant ssh
```

- Sign up for a Datadog account
- Install the Datadog agent using the provided command with unique api key:

`DD_API_KEY=<MYAPIKEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

# Collecting Metrics
- Add tags in the Agent config file and show a screenshot of your host and its tags on the Host Map page in Datadog.

`vagrant@ubuntu-xenial:/etc/datadog-agent$ sudo vi datadog.yaml`

Set the host tags to the following: 

```
tags:
   - vagrant_box
   - env:dev
   - aliciatest
   - role:server
```
For the tags to take effect, agent is restarted: 
`sudo service datadog-agent restart`

![Tags Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/host_tags_screenshot2.png)

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Follow instructions here to install MongoDB on Ubuntu: (https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04)

Configure mongodb for datadog: 

Follow instructions here to create a read-only user for the Datadog Agent in the admin database.
(https://docs.datadoghq.com/integrations/mongo/)

Edit the configuration yaml file for MongoDB in /etc/datadog-agent/conf.d:

`sudo vi conf.d/mongo.d/conf.yaml`

```
init_config:

instances:
  # Specify the MongoDB URI, with database to use for reporting (defaults to "admin")
  - server: mongodb://datadog:password@localhost:27017/admin
    additional_metrics:
      - collection
      - metrics.commands
      - tcmalloc
      - top
```

Edit conf.yaml to enable logs for MongoDB: 

```
logs:

  - type: file
    path: /var/log/mongodb/mongod.log
    service: mongo
    source: mongodb
```

Run the mongo check to verify that the check works properly: 
`sudo -u dd-agent -- datadog-agent check mongo`

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Create the custom check in /etc/datadog-agent/checks.d/
Contents of `my_metric.py`
```
import random
from checks import AgentCheck

class my_metric(AgentCheck):
    def check(self, instance):
        myrand = random.randint(1, 1000)
        #force NoData for testing
        #myrand = None
        self.gauge('my_metric', myrand)
```

- Change your check's collection interval so that it only submits the metric once every 45 seconds.
- Bonus Question Can you change the collection interval without modifying the Python check file you created?

I changed the collection interval for my_metric to 45 seconds by setting it in the check's yaml file.

Contents of `my_metric.yaml`
```
init_config:

instances:
    - min_collection_interval: 45
```

# Visualizing Data

1. Create an app key

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_createappkey.png)

2. Install datadog python library
`pip install datadog`

3. Write a Python script to create the timeboard using the datadog API: 

```
title = "Alicia Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric status"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.network.numrequestsps{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies in MongoDB Number of requests per second"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric sum of all points for the past hour"
}
]
```

- Timeboard showing past 4 hours: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_past4hours.png)

- Set the Timeboard's timeframe to the past 5 minutes
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_5mingraphs.png)

- Take a snapshot of this graph and use the @ notation to send it to yourself.

I highlighted the area of the graph with the anomaly and then sent a notification to myself: 

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_create_snapshot.png)

I received an email from Datadog with the snapshot annotation that I had created for the anomaly graph: 

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/snapshot_email.png)

- Bonus Question: What is the Anomaly graph displaying?
The anomaly graph shows a distinction between normal and abnormal trends in a series of data points. In this graph we can see that historically there has not been much acitvity in MongoDB requests, however there is an abnormal spike at 1.46 requests per second around the 15:25:36 timestamp.

# Monitoring

- Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes.

Email showing monitor alert triggered when value breached 500: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_warning_email.png)

Email showing monitor alert triggered when value breached 800: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_alert_email.png)

Email showing monitor alert triggered when value had No Data: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_nodata_email.png)


- Bonus Question - Setup scheduled downtimes

Silence from 7pm to 9am daily on M-F:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_start.png)

And one that silences it all day on Sat-Sun:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_weekends.png)


# Collecting APM Data

First install ddtrace.

`pip3 install ddtrace`

Create flask_app.py
```
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
    app.run(host='127.0.0.1', port='5050')

```

Enable APM monitoring in datadog.yml
```
# Trace Agent Specific Settings
#
apm_config:
#   Whether or not the APM Agent should run
  enabled: true
```

Run the application using ddtrace-run

`ddtrace-run python3 flask_app.py`

Then make some calls to the app's endpoints: 

```
wget 127.0.0.1:5050/api/trace
wget 127.0.0.1:5050/api/apm
wget 127.0.0.1:5050/
```

The trace is listed here for my flask app in the APM tab:
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/apm_list.png)

Here is the page showing APM metrics for my flask app: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/apm_flask_dashboard.png)

- Bonus Question: What is the difference between a Service and a Resource?

There can be multiple services such as a database, webapp, or api service. The collection of services together work to run a website with a backend database, for example. A resource is an individual action for a service such as the /api/trace endpoint. A resource could also be the query statement for a database service.

- Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
[Public Link to Dashboard](https://p.datadoghq.com/sb/63f58bd46-e7e11a63ecc57b7d1dc1e0679f020707)

# Final Question
- Is there anything creative you would use Datadog for?

I would use Datadog to collect metrics from my smart watch (or from cloud service) about my exercising statistics such as heart rate, calories burned, miles ran, etc. It would be interesting to capture trends over time. It would also allow me to create graphs to quickly spot areas where I am not exercising enough or too much.


