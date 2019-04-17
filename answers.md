
# Technical Interview Round - VP

## Introduction
Purpose of this document is to go through the steps to install, instrument and correlate metrics data using DataDog Agents for various integration points.

## Collecting Metrics:

### Step 1:
Instrument DataDog Infrastructure and APM Agents. In this step, I have installed the DataDog agents in Ubuntu and AWS versions of Linux.

> Installation in Linux is **very easy with one single command**. I must say this
> is the easiest installation method compared to other tools I have used.

```curl
DD_API_KEY=<KEY_GOES_HERE> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

##### Here is the reference of Host Map
![Host Map](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/hostmap.jpg)

##### Tags are added in AWS and Agent Configurations
![Adding Tags](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/tags.jpg)
![APM Tag](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-tag.jpg)

### Step 2:
I installed MySQL integration based on the instructions in documentation. The steps are very simple and easy as listed below;

* Create **mysql.yaml** file at this location: **/etc/datadog-agent/conf.d/mysql.d**
* I ran this command to create a yaml file ```sudo vi /etc/datadog-agent/conf.d/mysql.d/mysql.yaml ```
* Add this Information in the **mysql.yaml** file

  ``` yaml
  init_config:

    instances:
      - server: localhost
        user: datadog
        pass: KEY_GOES_HERE
        ```
* Restart the datadog agent. Use this command in linux ```sudo service datadog-agent restart```

Then I created the following dashboard to confirm that the DataDog MySQL integration agent is able to collect DB metrics from the host.

![MySQL integration](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/mysql-metrics.jpg)

### Step 3:
I created a custom agent to generate random metric point between **0 to 1000** by creating two individual files ```my_metric.yaml``` and ```my_metric.py``` at the following locations

![Custom Agent](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/custom_metric.jpg)

Contents of **my_metric.yaml** file located at **/etc/datadog-agent/conf.d**

  ``` yaml
init_config:

instances:
[{}]
```

Content of **my_metric.py** file located at **/etc/datadog-agent/checks.d**

``` Python
from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

# custom counter logic

from random import *

METRIC_NAME_PREFIX = "custom"

class MyMetric(AgentCheck):
    def check(self, instance):
        x = randint(0, 1000)    # Pick a random number between 0 and 1000.
        self.gauge('my_metric', x, tags=['env=production'])
```

**Bonus Question**: I changed the interval of custom metric collection in **my_metric.yaml** file instead of python script as suggest in the documentation to 45 seconds, such that it only submits the metric once every 45 seconds. [https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval)

``` yaml
init_config:

instances:
  - min_collection_interval: 45
```

## Visualizing Data:

### Step 3:
I created the following dashboards using APIs. I chose python libraries to automate CRUD functions via APIs. First, I added datadog api libraries to my host by using this command - ```pip install datadog```

#### Create a Dashboard

[Create Dashboard](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/scripts/dashboard-create.py)

``` Python
from datadog import initialize, api

options = {
    'api_key': 'KEY_GOES_HERE',
    'app_key': 'KEY_GOES_HERE'
}

initialize(**options)

title = 'MySQL Stats'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'Bin Log Disk Use'
    }
}]
layout_type = 'ordered'
description = 'MySQL DB Information via APIs'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )
```

Then I updated the dashboard using this API and added Anomalies detection as well as Roll up sum

#### Update Dashboard

[Update Dashboard](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/scripts/dashboard-update.py)

``` Python
from datadog import initialize, api

options = {
    'api_key': 'KEY_GOES_HERE',
    'app_key': 'KEY_GOES_HERE'
}

initialize(**options)

dashboard_id = '3zw-8gj-5pd'

title = 'My Metrics Updated'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'MySQL CPU Time'
                }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-08021c29f543d000a}'}
        ],
        'title': 'Last 1 hr Custom Metrics'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:my_metric{host:i-08021c29f543d000a}, 'basic', 2)"}
        ],
        'title': 'Anomaly Detection'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "sum:my_metric{host:i-08021c29f543d000a}.rollup(3600)"}
        ],
        'title': 'Metric Sum Roll Up'
                    }
    }
]

layout_type = 'ordered'
description = 'MySQL DB Information Updated'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.update(dashboard_id,
                     title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )
```
### Step 4:
Then I narrowed the time window to 5 minutes time slice by clicking and dragging on the chart
![5 Minutes Timeslice](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/narrow-5-min-window.jpg)

### Step 5:
Then I added annotation and sent metrics to myself by clicking on the metric chart and chose **Annotate this graph** option

![Annotate this graph](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/annotate-this-graph.jpg)

Type your message with ```@mention```

![Annotation](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/annotate.jpg)

### Step 6:

#### What is the Anomaly graph displaying?
The anomaly graph is used to identify the metric range. It help us to understand the abnormal behavior of the metric in a given environment by highlights the standard metric range in the chart in grey color and shows deviation from standards highlighted in red color.

## Monitoring Data:

### Step 7:
Metric Monitor : Specify the range of threshold while setting up a monitor

![Setup a new monitor](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/monitor-metric.jpg)

### Step 8:
Define different messages based on type of threshold and conditions

![Messages](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/custom-message-alert.jpg)

### Step 9:
I received Email notification as soon as the thresholds were met

![Email Notification](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/alert-notification.jpg)

### Step 10:
Monitor History with current incident

![Monitor History](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/alert-history.png)

### Step 11:
Scheduled Downtime

##### Daily downtime from 7 PM to 9 AM
Define scheduled downtime window between 7 PM - 9 AM during weekdays
![During weekday](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekday.jpg)

Define scheduled downtime window on Saturday and Sunday due to weekend
##### Weekend Snooze (Saturday and Sunday)
![During weekend](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekend.jpg)

## Collecting APM Data:
I instrumented PHP, Java, Ruby, Python applications to see the depth of APM instrumentation. Java APM agent was the fastest and easiest to instrument.

### Step 12
I used this command to install python agent  ```pip install ddtrace```

### Step 13
Here is the fully instrumented Python(Flask) script

``` Python
from flask import Flask
import logging
import sys

from datadog import initialize

options = {
    'api_key':'KEY',
    'app_key':'KEY'
}

initialize(**options)

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

### Step 14

Execute your newly created python script by running this command ```ddtrace-run python test.py ```

![Execute Python Script with APM](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/run-apm.jpg)

Summary View of APM Instrumentation

![APM Instrumentation](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-instrumentation.jpg)

## Final Question:
Ability to track the uptime of the servers and suggest end-users with a recommended power cycle approach might be a good idea to manage system resources. It avoids abnormal system behaviors such as freeze and slow responses due to in-memory resource consumption.  

## Links
[Dashboard Link](https://app.datadoghq.com/dashboard/kne-d3n-dvn/application--server-health?tile_size=m&page=0&is_auto=false&from_ts=1554656400000&to_ts=1554742800000&live=true)

[Monitor Link](https://app.datadoghq.com/monitors/9434143)

[Notebook Link](https://app.datadoghq.com/notebook/110047/Analysis-Notebook?cell=mnqavzkq)
