Personal Information

- Name: Adilson Somensari
- Email: somensari@gmail.com
- Datadog account: tomaso@italymail.com

---

# Collecting Metrics

## Tags
I created an Ubuntu VM and added tags to the config file /etc/datadog/datadog.yml

>
>tags:
>   - "environment:dev"
>   - "country:canada"
>   - "mytag:myvalue”
`

![dashboard](/host_tags_view.png)

## Custom Agent
I created a python script (exercise.yml) and placed it under the checks.d directory.

``` python
  try:
    from datadog_checks.base import AgentCheck
  except ImportError:
    from checks import AgentCheck

  from random import randrange

  __version__ = "1.0.0"

  class ExerciseCheck(AgentCheck):
    def check(self, instance):
        self.gauge('exercise.my_metric', randrange(0,1000), tags=['exercise:random'])
                                                             	
```
And I also created the exercise.yml file on the conf.d

``` yml
init_config:

instances:
  - min_collection_interval: 45            	
```

And configured the collection interval to 45 seconds as requested.

So the answer to the question is yes, you can change the interval without changing the python script. In fact, I actually have a question… Need to take a look at the docs later

I actually have a question: How the collection interval affects alerting (if at all)? Most monitoring/observability platforms have regular "harvest cycles" (15sec, 30 sec, 1 min) and configuring collection intervals that are large (5 min+) can affect metric aggregation and alert evaluation engines.

## Database
I configured a mysql instance on my box and configured the database monitoring by cloning the conf.yml file under conf.d/mysql.d directory and changing the database credentials

![dashboard](/mysql_dashboard.png)

# Visualizing Data

I created the Timeboard named "Exercise Timeboard", then I exported it to a file (dashboard.json), and created it again on Datadog using curl

``` bash
curl -X POST -H "Content-Type: application/json" -H "DD-API-KEY: ae9774213091cc6286446962c9de0fa6" -H "DD-APPLICATION-KEY: XXXXXXXXXXXXX" -d @dashboard.json "https://api.datadoghq.com/api/v1/dashboard"
```
I did set up the timeboard but I am not sure I did the rollup portion correctly. I need to review the documentation so I can wrap my head around the rationale there… maybe I need more/better data too.

**Bonus**: The anomaly chart is graphing the metrics and highlighting periods that "look" anomalous (values above or below the "expected" values)

![dashboard](/custom_metric_anomaly.png)

# Monitoring Data
Here's the threshold configuration
![dashboard](/monitor_definition1.png)

![dashboard](/monitor_definition2.png)
Here are the different messages according to severity and the host/ip/metric values


# Maintenance Windows
Created the maintenance windows as requested, see screenshots
![dashboard](/mmaintenance_windows.png)

# APM

I instrumented two apps:
Spring Pet Clinic (no code change, just using regular auto instrumentation)
Sample Flask App

Here’s the code for Flask App:

```python

from flask import Flask
import logging
import sys
from ddtrace import tracer

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@tracer.wrap()
@app.route('/')
def api_entry():
	return 'Entrypoint to the Application'

@tracer.wrap("apm",service="exercise-svc")
@app.route('/api/apm')
def apm_endpoint():
	return 'Getting APM Started'

@app.route('/error')
def errpr_endpoint():
	span = tracer.trace('operation')
	span.error = 1
	span.finish()
	return 'ERROR'

@app.route('/api/trace')
def trace_endpoint():
	return 'Posting Traces'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5555')

```

Here's the dashboard:
![dashboard](/apm_infra.png)

In a nutshell, a service defines an “ application” as it groups assets related to the application (db queries, endpoints, etc) and a resource is one of the “ components”  of a service (maybe a query, an instrumented endpoint, etc)

---

I had plans to setup a K8 cluster and deploy the agent, maybe try some logs and other things... synthetic checks/RUM... the platform is so vast and there's a lot to explore. We are, however, getting close to the end of the quarter and my availability is getting very limited... for that reason I decided to submit the exercise without the other "goodies".
Please contact me if you have questions.
Thanks,
Adilson

---
