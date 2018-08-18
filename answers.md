## Questions

## Prerequisites - Setup the environment

For my environment I have decided to use to Mac OS X 10.13.
Following the steps on found [here](https://app.datadoghq.com/account/settings#agent/mac)

```DD_API_KEY=<MY API KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"```

## Collecting Metrics:

Any time any configuration file is modified the DataDog Agent must be restarted. On OS X the commands are:

```launchctl stop com.datadoghq.agent```

```launchctl start com.datadoghq.agent```


in order to see the agent status use the command


```datadog-agent status```


In order to add custom tags you must begin by modifying the datadog config file found in: 


```/opt/datadog-agent/etc/datadog.yaml```


and adding the following tags:
![agent tags](https://i.imgur.com/QGayXNS.png)
I was able to find the newly added tags on my Datadog Host Map page.
![host map page](https://i.imgur.com/7TvCJvv.png)

The next step was to install a database. I chose to install MySQL since I am familiar with the process. I chose to use homebrew for the installation found [here](https://gist.github.com/spencercharest/fc1748808af1a7aa157e0eebb64926f6)

Following the steps found [here](https://app.datadoghq.com/account/settings#integrations/mysql) I created a datadog user:
![user creation](https://i.imgur.com/FZ1CoRc.png)

and gave that user proper permissions:
![permissions](https://i.imgur.com/7bhTf5a.png)

The next step was to configure the Datadog configure file found in:
```/opt/datadog-agent/etc/conf.d/mysql.d```
![conf file](https://i.imgur.com/sWsAiGY.png)

In order to verify that the mysql configuration was successful, I ran the command:
```datadog-agent status```
and found that the mysql check had passed:
![mysql check](https://i.imgur.com/A6NiDiS.png)

The next step to create a custom metric I needed to add a ```my_metric.yaml``` to the ```/opt/datadog-agent/etc/conf.d/``` directory:

![directory](https://i.imgur.com/e8DMkOk.png)

The ```min_collection_interval``` makes sure that the agent checks the metric at most once every 45 seconds versus the default 15 seconds. 

The next step was to create the python check file named ```my_metric.py```. The new file was located in:


```/opt/datadog-agent/etc/checks.d```


![python check file](https://i.imgur.com/9eDmZsQ.png)

I added the line of code ```self.log.info``` in order to verify the file was being checked every 45 seconds in the log output.
![log file](https://i.imgur.com/D3Llbh5.png)
![log file](https://i.imgur.com/3tpJSVS.png)
![log file](https://i.imgur.com/74CXu6J.png)

## Visualizing Data:
Python file for visualizing data:
```python
from datadog import initialize, api

options = {'api_key': '33f2066955f5f6d25d5f09397e361fc6',
           'app_key': 'ed30d834dc5f7067542bf500c9f6bf6b8081c75f'}

initialize(**options)


title = "My Custom Timeboard Challenge"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2, direction='above', alert_window='last_5m', interval=20, count_default_zero='true')"}
        ],
        "viz": "timeseries"
    },
    "title": "SQL CPU Performance Time"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 120)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric with Rollup Function"
},
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
                     template_variables=template_variables,
                     read_only=read_only)
```

The Dashboard can be seen in the Datadog Dashboard UI scoped over 5 minutes:
![dashboard](https://i.imgur.com/h7QcvYX.png)
Sending a snapshot to myself:

![snapshot](https://i.imgur.com/xfvKBbf.png)

The anomaly graph is displaying a moving average of where datadog expect the metric to fall within given the variable settings. 


## Monitoring Data
Next I created an alert that takes a 5 minute average:

-warns when the custom metric falls above 500

-alerts when the metric falls above 800

-notifies when no data has been collected for the past 10 minutes. 


The monitor settings are as follow:

![monitor](https://i.imgur.com/QTj8dqy.png)

![no activity](https://i.imgur.com/D8LZ8aw.png)

The custom message is as follows:
```
{{#is_warning}}
Your metric has gone above  {{warn_threshold}}! Your metric is {{value}} 
{{/is_warning}} 

{{#is_alert}}
For your host: {{host.name}} with IP {{host.ip}}, your metric is now above {{threshold}} Please Fix!! Your metric is {{value}} 
{{/is_alert}} 

{{#is_no_data}}
Your metric has stopped responding for 10 Minutes. 
{{/is_no_data}} 

Notify @michaelsenejoa@gmail.com
```

A snapshot of a warning email:
![warning email](https://i.imgur.com/2OP2TbQ.png)

Scheduled Monday-Friday 7PM-9AM Downtime:

![weekday downtime](https://i.imgur.com/EUh9Tzs.png)

Scheduled Weekend Downtime

![weekend downtime](https://i.imgur.com/xHQneXz.png)

## Collecting APM Data:
The first step was to install the Datadog APM agent found [here](https://github.com/DataDog/datadog-trace-agent#development)

The source code was downloaded using the command:


```go get -u github.com/DataDog/datadog-trace-agent/releases/download/6.4.1/trace-agent-darwin-amd64-6.4.1```


and installed the agent using the command:

```
cd $GOPATH/src/github.com/DataDog/datadog-trace-agent
make install
```

The Datadog config file then had to be modified in order to allow the AMP agent to collect information:
![config](https://i.imgur.com/C4xTkbV.png)

Once the agent is configured the next step is to download the two python dependencies using the commands:

```pip install ddtrace```

```pip install blinker```


and to modify the python file to include ddtrace in order to collect information as middleware. 

```python
from flask import Flask
import logging
import sys


from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware


# Have flask use stdout as the logger
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

The agent was then started using the command:


```$GOPATH/bin/trace-agent```


the python-flask server was started using the command:


```python apm_trace.py```


I then navigated my broswer to ```http://localhost:5050/``` and ```http://localhost:5050/api/apm``` in order to give the APM some metrics to read. I visualized the APM data with an included infrastructure metric: 
![metrics](https://i.imgur.com/Xv2rgE1.png)

with a public link to the screenboard found [here](https://p.datadoghq.com/sb/9194d43ca-e03ea8699c90b2e7aff37f4d3c09a3cc)

## Final Question
I was first introduced to DataDog when working as a Process/Production Engineer at shapeways. The factory instrumented a DataDog dashboards to show the status of PO’s in our production pipeline. It would also alert the team when a PO was in a specific status for too long in order to avoid lost orders. This type of monitoring is what got me interested in programming and automation. 

One of my favorite non-fiction books is called “Dataclysm”, it uses Big Data analytics to show how people act in various social media platforms. This book fascinated me and introduced me to a new field merging Big Data analytics and sociology. It would be very interesting to see DataDog applied to these fields, scrape data from social media and analyze general trends of social problems and how people react on social media.

The obvious implications of data analytics can be used in a countless amount of ways in almost every industry. In the new emerging field of vertical/automated farming, DataDog could be easily implemented to integrate with existing environmental monitors/sensors. In Blockchains/Crypto currencies Datadog could be used for automatic trading/trend analysis of transactional throughput of blockchain databases and servers. 

The uses for this type of technological infrastructure monitoring are countless and DataDog is leading the way. 

