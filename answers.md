## Prerequisites - Setup the environment
For the exercise I spin up a EC2 instance on AWS. OS = ubuntu 16.04.
Then I installed the Agent with the following command:

```
DD_API_KEY=your_api_key bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

## Collecting Metrics

### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I edited the _datadog.yaml_ (using ```sudo nano /etc/datadog-agent/datadog.yaml```) and I added some tags to the host:

```
tags:
   - environment:dev
   - service:microservice
   - project:myproject
```

Screenshot of my host and its tags on the Host Map page in Datadog:
![Host Map tags](./host_map_tags.PNG)

### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB and set up the Datadog integration.
First of all, add a new user to Mongo:

```
use admin
db.createUser({
  "user":"datadog",
  "pwd": "<******>",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
})
```

Then configure the Agent ( ```sudo nano /etc/datadog-agent/conf.d/mongo.d/conf.yaml```) adding the following:

```
init_config:
instances:
  - server: mongodb://datadog:datadog@localhost:27017/admin
    additional_metrics:
      - collection       # collect metrics for each collection
      - metrics.commands
      - tcmalloc
      - top
    tag:
      - project:myproject
```

Restart the Agent ```sudo service datadog-agent restart```.

Datadog integration for the database:
![MongoDb Apps](./mongodb_apps.PNG)

### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I created a new Python script (```my_metric.py```) in the folder ```/etc/datadog-agent/checks.d/```.

```python
import random
from checks import AgentCheck

class MyRandomValue(AgentCheck):
      def check(self, instance):
          self.gauge('my_random_value_metric', random.randint(1,1000),tags=['service:my_great_app'])
```

Then I created the configuration file ```my_metric.yaml ``` in the ```/etc/datadog-agent/conf.d/``` folder.

### Change your check's collection interval so that it only submits the metric once every 45 seconds.

Edit the ```/etc/datadog-agent/conf.d/my_metric.yaml```  file and add the following:
```
init_config:
instances:
  - min_collection_interval: 45
```
### Can you change the collection interval without modifying the Python check file you created?
Yes, see the previous answer.

## Visualizing Data

Utilize the Datadog API I created a Timeboard following the requirements.
Here the Python script:
```python
from datadog import initialize, api

def create_dashboard():

    options = {
        'api_key': '***********',
        'app_key': '***********'
    }
    initialize(**options)

    host_name = 'i-047e4230a19500e64'
    title = 'My new dashboard'
    widgets = [{
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': f'sum:my_random_value_metric{{host:{host_name}}}'}
            ],
            'title': 'my_random_value_metric'
            }
    },{
        'definition': {
            'type': 'timeseries',
            'requests': [
                    {'q': f'sum:my_random_value_metric{{host:{host_name}}}.rollup(sum, 3600)'}
            ],
            'title': 'my_random_value_metric rollup 1h'
            }
    },{
        'definition': {
            'type': 'timeseries',
            'requests': [
                    {"q": f"anomalies(avg:mongodb.mem.resident{{host:{host_name}}}, 'basic', 2)"}
            ],
            'title': 'Mongodb mongodb.mem.resident anomalies'
            }
    }]

    layout_type = 'ordered'
    description = 'My new dashboard description'
    notify_list = ['zuccon.matteo@gmail.com']
    api.Dashboard.create(title=title,
                        widgets=widgets,
                        layout_type=layout_type,
                        description=description,
                        is_read_only=False,
                        notify_list=notify_list)

if __name__ == "__main__":
    create_dashboard()
```

Here the dashboard from Datadog UI:
![dashboard](./dashboard.PNG)
Snapshot of a graph sent to myself using the @ notation.
![dashboard_snapshot](./snapshot.PNG)
![dashboard_snapshot_email](./dashboard_snapshot.PNG)

### What is the Anomaly graph displaying?
The anomaly graph is showing the anomaly for the amount of memory currently used by the database process (mongodb).

## Monitoring Data

I created a new metric monitor following the given requirements (threshold).
![metric monitor](./metric_monitor.PNG)

Email received:
![email](./Email_Warning_Monitoring.PNG)

Scheduled downtimes for the monitor:

![metric monitor silence](./monitor_silence1.PNG)
![metric monitor silence email](./monitor_silence_email.PNG)

![metric monitor silence](./monitor_silence2.PNG)
![metric monitor silence email](./monitor_silence_email2.PNG)

## Collecting APM Data

I run the following script
```python
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
    app.run(host='0.0.0.0', port='5050')
```
using ```ddtrace-run python app.py``` (remember to run ```pip install ddtrace```)

### What is the difference between a Service and a Resource?
A service is a set of processes that do the same job.
A Resource is a particular action for a service.
Reference: https://docs.datadoghq.com/tracing/visualization/

![APM dashboard](./APM_Dashboard.PNG)

I could now find a way to share publicly a timeboard, so I created a screenboard: https://p.datadoghq.com/sb/47zdzqypwc7ie1h3-b7b12b4b7d6e1c9429e9c005053c39a1

## Final Question

Right now in Milan, free standing bikes and scooters are becoming very popular.
It would be nice to monitor how people move around, 
how fast they go, which is the best (most used/fastest) route to get from point A to point B and integrate these metrics with APP usage (to optimize the service).






