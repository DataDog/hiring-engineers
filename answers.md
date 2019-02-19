Your answers to the questions go here.

## Step 1) Setting up environment

I first installed and set up my python environment to proceed with the task. I installed the virtualenvwrapper as shown below:

![image](https://user-images.githubusercontent.com/38798668/52760757-accef400-2fde-11e9-85fb-f795fff453e4.png)

Ran into an uninstall six error (the first of many roadblocks =]). Fixed this issue by utilizing the following command:

```
sudo pip install tld --ignore-installed six
```

Used the following to work on my chosen env

```
workon datadog
```

![image](https://user-images.githubusercontent.com/38798668/52760870-26ff7880-2fdf-11e9-9e0e-c394322871d3.png)


## Step 2) Collecting Metrics

Initial test run tag with Host Map showing:

![image](https://user-images.githubusercontent.com/38798668/52766734-1dcdd600-2ff6-11e9-8caf-d5cfcd0c51c7.png)

Tags I updated after initial test run

![image](https://user-images.githubusercontent.com/38798668/52766702-ff67da80-2ff5-11e9-97e4-7bfcb8ac0ec5.png)


I already had Postgres installed on my machine previously. Updated postgres.yaml file

```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: cYkSGd4SUh8lNt5xrE7AHnSg
    tags:
      - db:staging:pg
```

Postgres Ok

![image](https://user-images.githubusercontent.com/38798668/52760835-fd465180-2fde-11e9-9b41-cdad13c693a9.png)

Set up my custom metric check called custom_metric_checl with a random value between 0 and 1000

```py
from datadog_checks.checks import AgentCheck
from random import randint

__version__ = "1.0.0"


class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom_my_metric', randint(0, 1000))
```

I changed my check collection interval so that it only submits the metric once every 45 seconds

![image](https://user-images.githubusercontent.com/38798668/52767301-114a7d00-2ff8-11e9-9127-53ac3cafc299.png)

#### Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes! Instead of modifying the python file, you utilize the min_collection_interval for your custom metric check yaml file and set it to 45(seconds)

```yaml
init_config:

instances:
  - min_collection_interval: 45

```

## Step 3) Visualizing Data

1. Utilize the Datadog API to create a Timeboard.

I looked at the API documentation in order to figure out the format of sending my python script.
Here is the timeboard created with the 3 graphs:

![image](https://user-images.githubusercontent.com/38798668/52770177-69857d00-3000-11e9-94c8-9bab4b442b3a.png)

I used the following script to render the charts:

```py
from datadog import initialize, api

options = {
  #Put in your own api and app key
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

title = "My Timeboard"
description = "Custom Metric Timeboards."
graphs = [{
  # custom metric scoped over my host
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom_my_metric{host:Josephs-MBP-2.fios-router.home}"},
        ],
        "viz": "timeseries"
    },
    "title": "Custom My Metric Timeseries"
},
{# chosen metric from my db using the anomaly function
      "definition": {
        "events": [],
        "requests": [
             {"q": "anomalies(avg:system.cpu.system{*}, 'basic', 2)"},
        ],
        "viz": "timeseries"
    },
    "title": "CPU Anomalies "
},
{# custom metric w/ rollup function applied to sum up all points for the past hour
      "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom_my_metric{*}.rollup(sum, 3600)"},
        ],
        "viz": "query_value"
    },
    "title": "Custom Metric Rollup Sum"
}]

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

2. Once this is created, access the Dashboard from your Dashboard List in the UI:

Here is the 5 min time frame of my custom metric graph

![image](https://user-images.githubusercontent.com/38798668/52770588-83738f80-3001-11e9-9c93-4ad39e0c98ef.png)

Here is the snapshot that was sent to my email

![image](https://user-images.githubusercontent.com/38798668/52770725-dcdbbe80-3001-11e9-87df-f8c256b60ce4.png)


### Bonus Question: What is the Anomaly graph displaying?
Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week,and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

It is showing a gray band which represents the deviations or the bounds parameter that is used in the anomalies function

## Step 4) Monitoring Data

Set my metric monitor configuration using the gui to send me a warning, alerting and no data notice.

![image](https://user-images.githubusercontent.com/38798668/52771441-e49c6280-3003-11e9-8acb-d2ddaa842de5.png)

Here is my email notification set up

![image](https://user-images.githubusercontent.com/38798668/52771441-e49c6280-3003-11e9-8acb-d2ddaa842de5.png)

History of monitor graph

![image](https://user-images.githubusercontent.com/38798668/52771566-38a74700-3004-11e9-86fb-a4200a3d48c0.png)

Email of Monitor Warning
![image](https://user-images.githubusercontent.com/38798668/52814909-48a64180-306b-11e9-9b7a-7224abbd4182.png)

### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

I set up two scheduled downtimes. The first one silences it from 7pm to 9am daily on M-F:
![image](https://user-images.githubusercontent.com/38798668/52814623-92daf300-306a-11e9-8b3f-d4551c8cba06.png)

![image](https://user-images.githubusercontent.com/38798668/52814725-cddd2680-306a-11e9-8be5-babb26645b9a.png)


The second silences it all day on Sat-Sun
![image](https://user-images.githubusercontent.com/38798668/52814674-aede9480-306a-11e9-86f4-e9b2ffe1db33.png)


Here is the email notification

![image](https://user-images.githubusercontent.com/38798668/52814832-1dbbed80-306b-11e9-8a38-c6b5285ff093.png)

## Step 5) Collecting APM Data

I followed the docs and set up the APM via a long and arduous journey. I was able to finally defeat that foul bug after many hours of scouring the docs and playing with all the configurations. I played around with the apm configurations in my datadog.yaml file and installed ddtrace and flask on my datadog virtualenv utilizing the following commands.
```
workon datadog
```

```
pip install ddtrace
```

I also set up flask

```
pip install flask
```

Updated my datadog.yaml file as shown

```yaml
apm_config:
  enabled: true
  analyzed_spans:
    flask|flask.request: 1
```
Here is my  initial app.py code

```py
from flask import Flask
# from ddtrace import patch_all
# patch_all()
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
    print('In app.py __main__')
    app.run(host='0.0.0.0', port='5050')

```


My flask was running as shown below

![image](https://user-images.githubusercontent.com/38798668/52815990-2530c600-306e-11e9-9d03-17f100e49c69.png)


I tried running it manually and using ddtrace separately but I ran into the following issue.
![image](https://user-images.githubusercontent.com/38798668/52815929-f61a5480-306d-11e9-8388-1111e17ce435.png)

```
ddtrace.writer - ERROR - cannot send spans to localhost:8126: [Errno 61] Connection refused
```

I decided to try a containerized approach. I set up the integration on my account and installed Docker. I did an intial test run to see if my docker container was running as shown below
![image](https://user-images.githubusercontent.com/38798668/53001638-23159100-33f9-11e9-9520-7585c80e4247.png)

![image](https://user-images.githubusercontent.com/38798668/52943177-8a204080-333a-11e9-890f-d36bd90fe0d2.png)

I tested out the requests manually but couldn't figure out why it wasn't showing up my datadog dashboard
![image](https://user-images.githubusercontent.com/38798668/52979810-54fd0800-33a5-11e9-9727-3209842988cf.png)
![image](https://user-images.githubusercontent.com/38798668/52979778-2b43e100-33a5-11e9-9b19-01d4583650a3.png)

I restarted the datadog agent and saw my APM traces were active. Here are the many steps that resulted in the successful setup. I updated my app.py code after digging through the documentation. I used the following commands to set up my virtualenv

```
pip install blinker
```
```
pip install requests
```

```py
from flask import Flask
from ddtrace import tracer, patch_all, config
patch_all(flask=True, requests=True)
import blinker as _
import logging
import sys
import os
import requests
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

tracer.configure(hostname='localhost')

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="flask_app")

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
    print('In app.py __main__')
    app.run(host='127.0.0.1', port='8126')
```
I initially made an error with the docker container so I checked for the container and I used the following command to find the specific container

```
docker container ls -a
```

I removed the container using the following command

```
docker container rm [CONTAINER ID]
```

I ran the updated command for docker integration

```
docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro \
            -v /proc/:/host/proc/:ro \
            -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
            -e DD_API_KEY=3bbb7f03d9149346d029d93eced23910 \
            -e DD_APM_ENABLED=true \
            -e DD_APM_NON_LOCAL_TRAFFIC=true \
            -e DD_APM_ANALYZED_SPANS="flask|flask.request=1"
            -p 8126:8126/tcp \
            datadog/agent:latest \
```
After checking that my docker container was running I ran the following command to launch the flask app

```
code .zshrc
```

```
# Flask App for Datadog
function dataflask() {
  export FLASK_APP=/Users/joe/.datadog-agent/app.py
  export FLASK_ENV=development
  ddtrace-run flask run --host=0.0.0.0 --port=8000
}
```
I sourced my .zshrc after making the changes

```
source ~/.zshrc
```

Here are the images for the successful run of the APM
![image](https://user-images.githubusercontent.com/38798668/52985112-44a65680-33c0-11e9-8734-bdc237236369.png)
![image](https://user-images.githubusercontent.com/38798668/52985373-8f749e00-33c1-11e9-98ff-88b559c1bcd9.png)
![image](https://user-images.githubusercontent.com/38798668/53000672-e8125e00-33f6-11e9-8a10-4faa3aa34cbc.png)

I loaded all the graphs onto my timeboard which can be seen below
![image](https://user-images.githubusercontent.com/38798668/53001309-4db31a00-33f8-11e9-8f65-8ee16e7529a1.png)

I made a screenboard that I can show the APM metrics and some of the other charts
![image](https://user-images.githubusercontent.com/38798668/53009397-6d9f0980-3409-11e9-8f7b-4f264b734894.png)

The link for this url is below

```
https://p.datadoghq.com/sb/09loq3vwd22vwo7d-3b74b8f02720d5147e836c6a64b27615
```
I felt very satisfied being able to work through the numerous bugs I encountered in this journey. A very rewarding experience being able to problem solve and scour the docs.

### Bonus Question: What is the difference between a Service and a Resource?

1. Services are a set of processes that do the same job.
2. Resources - A resource is a particular action for a service. An example would be a database query in the database of your choice that is associated with the application


## Final Question: Is there anything creative you would use Datadog for?

I have been fascinated with the financial sector for many years so I have a bias in utilizing Datadog for testing automated trading strategies. Having paid through college via day trading and fundamental investing, I fell in love with all the streaming data and the configurations available for charting, trade alerts, and many more. I would be interested in somehow implementing Datadog for future high frequency traders to keep track of their application. This would be ideal for use in coding bootcamps that focus on data science since the programmers would be notified of any unusual trades occurring or unusual spikes in market trading volume. Future traders could somehow monitor market fluctuations such as unusual volatility and seasonal trends. This would assist in tweaking their trading models and adjust accordingly.
